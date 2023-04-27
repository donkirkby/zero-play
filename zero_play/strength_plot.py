from io import StringIO
from multiprocessing import Process, Queue
import logging
from queue import Empty
import re
import typing

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
from matplotlib.animation import FuncAnimation
from sqlalchemy.orm import Session as BaseSession

# from zero_play.connect4.neural_net import NeuralNet
from zero_play.game_state import GameState as Game, GameState
from zero_play.mcts_player import MctsPlayer
from zero_play.models import SessionBase
from zero_play.models.game import GameRecord
from zero_play.models.match import MatchRecord
from zero_play.models.match_player import MatchPlayerRecord
from zero_play.models.player import PlayerRecord
from zero_play.play_controller import PlayController
from zero_play.playout import Playout
from zero_play.plot_canvas import PlotCanvas
from zero_play.tictactoe.state import TicTacToeState

logger = logging.getLogger(__name__)


class MatchUp:
    def __init__(self,
                 p1_definition: int | str | None = None,
                 p2_definition: int | str | None = None,
                 source: typing.Optional['MatchUp'] = None):
        if source is None:
            self.p1_iterations, self.p1_neural_net = MatchUp.parse_definition(
                p1_definition)
            self.p2_iterations, self.p2_neural_net = MatchUp.parse_definition(
                p2_definition)
            self.p1_wins = 0
            self.ties = 0
            self.p2_wins = 0
        else:
            self.p1_iterations = source.p1_iterations
            self.p1_neural_net = source.p1_neural_net
            self.p2_iterations = source.p2_iterations
            self.p2_neural_net = source.p2_neural_net
            self.p1_wins = source.p1_wins
            self.ties = source.ties
            self.p2_wins = source.p2_wins

    @staticmethod
    def parse_definition(definition):
        match = re.fullmatch(r'(\d+)(nn)?', str(definition))
        return int(match.group(1)), bool(match.group(2))

    @staticmethod
    def format_definition(iterations, neural_net):
        if neural_net:
            return f'{iterations}nn'
        return iterations

    def __repr__(self):
        p1_definition = self.format_definition(self.p1_iterations,
                                               self.p1_neural_net)
        p2_definition = self.format_definition(self.p2_iterations,
                                               self.p2_neural_net)
        return f'MatchUp({p1_definition!r}, {p2_definition!r})'

    @property
    def key(self):
        return (self.p1_iterations,
                self.p1_neural_net,
                self.p2_iterations,
                self.p2_neural_net)

    @property
    def count(self):
        return self.p1_wins + self.ties + self.p2_wins

    @property
    def p1_win_rate(self):
        return self.p1_wins / self.count if self.count else 0.

    @property
    def tie_rate(self):
        return self.ties / self.count if self.count else 0.

    @property
    def p2_win_rate(self):
        return self.p2_wins / self.count if self.count else 0.

    def record_result(self, result):
        if result < 0:
            self.p2_wins += 1
        elif result == 0:
            self.ties += 1
        else:
            self.p1_wins += 1


class WinCounter(dict):
    def __init__(self,
                 player_levels: typing.List[int] | None = None,
                 opponent_min: int | None = None,
                 opponent_max: int | None = None,
                 source: typing.Optional['WinCounter'] = None,
                 player_definitions: typing.List[str | int] | None = None):
        super().__init__()
        if source is not None:
            self.player_definitions: typing.List[
                typing.Union[str, int]] = source.player_definitions[:]
            self.opponent_levels: typing.List[int] = source.opponent_levels[:]
            for key, match_up in source.items():
                self[key] = MatchUp(source=match_up)
        else:
            if player_levels is not None:
                player_definitions = []
                for player_level in player_levels:
                    player_definitions.append(player_level)
            assert player_definitions is not None
            assert opponent_min is not None
            assert opponent_max is not None
            self.player_definitions = player_definitions[:]
            self.opponent_levels = []
            opponent_level = opponent_min
            while opponent_level <= opponent_max:
                self.opponent_levels.append(opponent_level)
                opponent_level <<= 1

            for player_definition in player_definitions:
                for opponent_level in self.opponent_levels:
                    match_up = MatchUp(player_definition, opponent_level)
                    self[match_up.key] = match_up
                    match_up = MatchUp(opponent_level, player_definition)
                    self[match_up.key] = match_up

    def find_next_matchup(self) -> MatchUp:
        best_matchup: typing.Optional[MatchUp] = None
        lowest_count = None
        for matchup in self.values():
            if best_matchup is None or matchup.count < lowest_count:
                best_matchup = matchup
                lowest_count = matchup.count

        assert best_matchup is not None
        return best_matchup

    def build_series(self):
        all_series = []
        for player_definition in self.player_definitions:
            parsed_player = MatchUp.parse_definition(player_definition)
            series = (f'wins as 1 with {player_definition}',
                      [self[parsed_player +
                            MatchUp.parse_definition(opponent_level)].p1_win_rate
                       for opponent_level in self.opponent_levels])
            all_series.append(series)
            series = (f'ties as 1 with {player_definition}',
                      [self[parsed_player +
                            MatchUp.parse_definition(opponent_level)].tie_rate
                       for opponent_level in self.opponent_levels])
            all_series.append(series)
            series = (f'wins as 2 with {player_definition}',
                      [self[MatchUp.parse_definition(opponent_level) +
                            parsed_player].p2_win_rate
                       for opponent_level in self.opponent_levels])
            all_series.append(series)
            series = (f'ties as 2 with {player_definition}',
                      [self[MatchUp.parse_definition(opponent_level) +
                            parsed_player].tie_rate
                       for opponent_level in self.opponent_levels])
            all_series.append(series)
        return all_series

    def build_summary(self):
        summary = StringIO()
        all_series = self.build_series()
        print('opponent levels', np.array(self.opponent_levels), file=summary)
        for i, player_definition in enumerate(self.player_definitions):
            for j in range(2):
                if j:
                    counts = [self[MatchUp.parse_definition(opponent_level) +
                                   MatchUp.parse_definition(player_definition)].count
                              for opponent_level in self.opponent_levels]
                    print('counts as 2 with',
                          player_definition,
                          np.array(counts),
                          file=summary)
                else:
                    counts = [self[MatchUp.parse_definition(player_definition) +
                                   MatchUp.parse_definition(opponent_level)].count
                              for opponent_level in self.opponent_levels]
                    print('counts as 1 with',
                          player_definition,
                          np.array(counts),
                          file=summary)
                for k in range(i * 4 + j * 2, i * 4 + (j + 1) * 2):
                    name, rates = all_series[k]
                    percentages = (np.array(rates) * 100).round().astype(int)
                    print(name, percentages, file=summary)
        return summary.getvalue()


class StrengthPlot(PlotCanvas):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.game: GameState = TicTacToeState()
        self.artists: typing.List[plt.Artist] = []
        self.plot_lines: typing.List[plt.Line2D] = []

        self.win_counter: WinCounter | None = None
        self.request_queue: Queue[str] = Queue()
        self.result_queue: Queue[
            typing.Tuple[int, bool, int, bool, int]] = Queue()
        self.db_session: BaseSession | None = None
        self.process: Process | None = None
        self.animation = FuncAnimation(self.axes.figure,
                                       self.update,
                                       interval=30_000,
                                       cache_frame_data=False)
        self.animation.pause()

    def start(self,
              db_session: BaseSession,
              controller: PlayController,
              player_definitions: typing.List[typing.Union[str, int]],
              opponent_min: int,
              opponent_max: int):
        self.db_session = db_session
        self.game = controller.start_state
        self.win_counter = WinCounter(player_definitions=player_definitions,
                                      opponent_min=opponent_min,
                                      opponent_max=opponent_max)
        self.load_history(db_session)
        # self.game_name = controller.start_state.game_name
        self.process = Process(target=run_games,
                               args=(controller,
                                     self.request_queue,
                                     self.result_queue,
                                     WinCounter(source=self.win_counter),
                                     # neural_net_path),
                                     ),
                               daemon=True)
        self.process.start()
        # self.worker_thread.start()
        sn.set()
        self.create_plot()
        plt.tight_layout()
        self.animation.resume()

    def stop_workers(self):
        self.request_queue.put('Stop')
        self.animation.pause()

    def fetch_strengths(self, db_session) -> typing.List[int]:
        if db_session is None:
            return []
        game_record = GameRecord.find_or_create(db_session, self.game)
        strengths = []
        datetimes = []
        match: MatchRecord
        # noinspection PyTypeChecker
        for match in game_record.matches:  # type: ignore
            match_player: MatchPlayerRecord
            # noinspection PyTypeChecker
            for match_player in match.match_players:  # type: ignore
                player = match_player.player
                if player.type != player.HUMAN_TYPE:
                    assert player.iterations is not None
                    strengths.append(player.iterations)
                    datetimes.append(match.start_time)
        return strengths

    def requery(self, db_session: SessionBase | None, future_strength: int):
        strengths = self.fetch_strengths(db_session)

        self.axes.clear()
        marker = 'o' if len(strengths) == 1 else ''
        self.axes.plot(strengths, marker, label='past')
        self.axes.plot([len(strengths)], [future_strength], 'o', label='next')
        self.axes.set_ylim(0)
        if len(strengths) + 1 < len(self.axes.get_xticks()):
            self.axes.set_xticks(list(range(len(strengths) + 1)))
        self.axes.set_title('Search iterations over time')
        self.axes.set_ylabel('Search iterations')
        self.axes.set_xlabel('Number of games played')
        self.axes.legend(loc='lower right')
        self.axes.figure.canvas.draw()

    # noinspection PyMethodOverriding
    def update(self, _frame=None) -> None:  # type: ignore
        messages = []
        try:
            for _ in range(1000):
                messages.append(self.result_queue.get_nowait())
        except Empty:
            pass
        # logger.debug('Plotter.update() found %d messages.', len(messages))
        if not messages:
            return
        assert self.win_counter is not None
        for p1_iterations, p1_nn, p2_iterations, p2_nn, result in messages:
            match_up: MatchUp = self.win_counter[(p1_iterations,
                                                  p1_nn,
                                                  p2_iterations,
                                                  p2_nn)]
            match_up.record_result(result)
            self.write_history(match_up, result)

        self.artists.clear()

        self.create_plot()
        self.axes.figure.canvas.draw()
        # logger.debug('Plotter.update() done.')
        # return self.artists

    def create_plot(self):
        opponent_levels = self.win_counter.opponent_levels
        all_series = self.win_counter.build_series()
        total_games = sum(match_up.count for match_up in self.win_counter.values())
        self.artists.append(self.axes.set_title(
            f'Win Rates After {total_games} '
            f'Games of {self.game.game_name}'))
        if not self.plot_lines:
            self.axes.set_ylabel(f'Win and tie rates')
            self.axes.set_xlabel('Opponent MCTS simulation count')
            self.axes.set_xscale('log')
            self.axes.set_ylim(-0.01, 1.01)
            group_num = 0
            prev_iter_count = ''
            for name, rates in all_series:
                fields = name.split()
                iter_count = fields[-1]
                if iter_count != prev_iter_count:
                    group_num += 1
                    prev_iter_count = iter_count
                player = fields[2]
                result = fields[0]
                match (result, player):
                    case 'ties', '1':
                        style = ':'
                    case 'ties', '2':
                        style = '-.'
                    case 'wins', '2':
                        style = '--'
                    case _:
                        style = ''
                style += f'C{group_num}'

                line, = self.axes.plot(opponent_levels, rates, style, label=name)
                self.plot_lines.append(
                    line)
            self.axes.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        else:
            for line, (name, rates) in zip(self.plot_lines, all_series):
                # noinspection PyTypeChecker
                line.set_ydata(rates)
        self.artists.extend(self.plot_lines)
        self.axes.redraw_in_frame()

        return self.artists

    def load_history(self, db_session: BaseSession):
        assert self.win_counter is not None
        player1_number = self.game.get_active_player()
        game_record = GameRecord.find_or_create(db_session, self.game)
        match_record: MatchRecord
        for match_record in game_record.matches:  # type: ignore
            player1_iterations = player2_iterations = result = None
            has_human = False
            match_player: MatchPlayerRecord
            for match_player in match_record.match_players:  # type: ignore
                player: PlayerRecord = match_player.player
                if player.type == PlayerRecord.HUMAN_TYPE:
                    has_human = True
                player_number = match_player.player_number
                if player_number == player1_number:
                    player1_iterations = player.iterations
                    result = match_player.result
                else:
                    player2_iterations = player.iterations
            if has_human:
                continue
            match_up = self.win_counter.get((player1_iterations,
                                             False,
                                             player2_iterations,
                                             False))
            if match_up is not None:
                match_up.record_result(result)
        print(self.win_counter.build_summary(), end='')

    def write_history(self, match_up: MatchUp, result: int):
        db_session = self.db_session
        assert db_session is not None
        game_record = GameRecord.find_or_create(db_session, self.game)
        match_record = MatchRecord(game=game_record)
        db_session.add(match_record)
        mcts_player: typing.Optional[MctsPlayer]
        iteration_entries = (match_up.p1_iterations, match_up.p2_iterations)
        for i, player_number in enumerate(self.game.get_players()):
            iterations = iteration_entries[i]
            player_record = db_session.query(PlayerRecord).filter_by(
                type=PlayerRecord.PLAYOUT_TYPE,
                iterations=iterations).one_or_none()
            if player_record is None:
                player_record = PlayerRecord(type=PlayerRecord.PLAYOUT_TYPE,
                                             iterations=iterations)
                db_session.add(player_record)
            player_result = result if i == 0 else -result
            match_player = MatchPlayerRecord(match=match_record,
                                             player=player_record,
                                             player_number=player_number,
                                             result=player_result)
            db_session.add(match_player)
        db_session.commit()


def run_games(controller: PlayController,
              request_queue: Queue,
              result_queue: Queue,
              win_counter: WinCounter,
              # checkpoint_path: str = None,
              game_count: int | None = None):
    """ Run a series of games, and send the results through a queue.

    :param controller: tracks game progress
    :param request_queue: source of control requests. For now, any message will
        tell this process to shut down.
    :param result_queue: destination for game results. Each message is a tuple
        with the match-up key and the game result: 1, 0, or -1 for player 1.
    :param win_counter: defines all the strength combinations to test.
    :param game_count: number of games to run, or None to run until stopped.
    """
    player1 = controller.players[Game.X_PLAYER]
    player2 = controller.players[Game.O_PLAYER]
    assert isinstance(player1, MctsPlayer)
    assert isinstance(player2, MctsPlayer)

    # nn = None
    playout = Playout()

    while game_count is None or game_count > 0:
        match_up = win_counter.find_next_matchup()
        player1.iteration_count = match_up.p1_iterations
        # if match_up.p1_neural_net:
        #     nn = nn or load_neural_net(controller.game, checkpoint_path)
        #     player1.heuristic = nn
        # else:
        player1.heuristic = playout
        player2.iteration_count = match_up.p2_iterations
        # if match_up.p2_neural_net:
        #     nn = nn or load_neural_net(controller.game, checkpoint_path)
        #     player2.heuristic = nn
        # else:
        player2.heuristic = playout
        # logger.debug(f'checking params {i}, {j} ({x}, {y}) with {counts[i, j]} counts')
        controller.start_game()
        while not controller.take_turn():
            try:
                request_queue.get_nowait()
                return  # Received the quit message.
            except Empty:
                pass

        if controller.board.is_win(Game.X_PLAYER):
            result = Game.X_PLAYER
        elif controller.board.is_win(Game.O_PLAYER):
            result = Game.O_PLAYER
        else:
            result = 0

        logger.debug('Result of pitting %s vs %s: %s.',
                     match_up.format_definition(match_up.p1_iterations,
                                                match_up.p1_neural_net),
                     match_up.format_definition(match_up.p2_iterations,
                                                match_up.p2_neural_net),
                     result)
        result_queue.put(match_up.key + (result,))
        match_up.record_result(result)
        if game_count:
            game_count -= 1


# def load_neural_net(game, checkpoint_path):
#     nn = NeuralNet(game)
#     if checkpoint_path:
#         nn.load_checkpoint(filename=checkpoint_path)
#     return nn
