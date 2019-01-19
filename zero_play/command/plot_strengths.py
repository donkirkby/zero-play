import logging
from io import StringIO

import numpy as np
import os
import sqlite3
import typing
from argparse import ArgumentDefaultsHelpFormatter, Namespace
from multiprocessing import Process, Queue
from queue import Empty
from sqlite3 import OperationalError

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sn

from zero_play.command.play import PlayController
from zero_play.game import Game
from zero_play.mcts_player import MctsPlayer
from zero_play.command_parser import CommandParser

logger = logging.getLogger(__name__)


class MatchUp:
    def __init__(self,
                 p1_iterations: int = None,
                 p2_iterations: int = None,
                 source: 'MatchUp' = None):
        if source is None:
            self.p1_iterations = p1_iterations
            self.p2_iterations = p2_iterations
            self.p1_wins = 0
            self.ties = 0
            self.p2_wins = 0
        else:
            self.p1_iterations = source.p1_iterations
            self.p2_iterations = source.p2_iterations
            self.p1_wins = source.p1_wins
            self.ties = source.ties
            self.p2_wins = source.p2_wins

    def __repr__(self):
        return f'MatchUp({self.p1_iterations}, {self.p2_iterations})'

    @property
    def key(self):
        return self.p1_iterations, self.p2_iterations

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
                 player_levels: typing.List[int] = None,
                 opponent_min: int = None,
                 opponent_max: int = None,
                 source: 'WinCounter' = None):
        super().__init__()
        if source is not None:
            self.player_levels = source.player_levels[:]
            self.opponent_levels = source.opponent_levels[:]
            for key, match_up in source.items():
                self[key] = MatchUp(source=match_up)
        else:
            self.player_levels = player_levels[:]
            self.opponent_levels = []
            opponent_level = opponent_min
            while opponent_level <= opponent_max:
                self.opponent_levels.append(opponent_level)
                opponent_level <<= 1

            for player_level in player_levels:
                for opponent_level in self.opponent_levels:
                    match_up = MatchUp(player_level, opponent_level)
                    self[match_up.key] = match_up
                    match_up = MatchUp(opponent_level, player_level)
                    self[match_up.key] = match_up

    def find_next_matchup(self) -> MatchUp:
        best_matchup = None
        lowest_count = None
        for matchup in self.values():
            if best_matchup is None or matchup.count < lowest_count:
                best_matchup = matchup
                lowest_count = matchup.count
        return best_matchup

    def build_series(self):
        all_series = []
        for player_level in self.player_levels:
            series = (f'wins as 1 with {player_level}',
                      [self[(player_level, opponent_level)].p1_win_rate
                       for opponent_level in self.opponent_levels])
            all_series.append(series)
            series = (f'ties as 1 with {player_level}',
                      [self[(player_level, opponent_level)].tie_rate
                       for opponent_level in self.opponent_levels])
            all_series.append(series)
            series = (f'wins as 2 with {player_level}',
                      [self[(opponent_level, player_level)].p2_win_rate
                       for opponent_level in self.opponent_levels])
            all_series.append(series)
            series = (f'ties as 2 with {player_level}',
                      [self[(opponent_level, player_level)].tie_rate
                       for opponent_level in self.opponent_levels])
            all_series.append(series)
        return all_series

    def build_summary(self):
        summary = StringIO()
        all_series = self.build_series()
        print('opponent levels', np.array(self.opponent_levels), file=summary)
        for i, player_level in enumerate(self.player_levels):
            for j in range(2):
                if j:
                    counts = [self[(opponent_level, player_level)].count
                              for opponent_level in self.opponent_levels]
                    print('counts as 2 with',
                          player_level,
                          np.array(counts),
                          file=summary)
                else:
                    counts = [self[(player_level, opponent_level)].count
                              for opponent_level in self.opponent_levels]
                    print('counts as 1 with',
                          player_level,
                          np.array(counts),
                          file=summary)
                for k in range(i * 4 + j * 2, i * 4 + (j + 1) * 2):
                    name, rates = all_series[k]
                    percentages = (np.array(rates) * 100).round().astype(int)
                    print(name, percentages, file=summary)
        return summary.getvalue()


class Plotter:
    def __init__(self,
                 db_path,
                 game_name: str,
                 controller: PlayController,
                 player_levels: typing.List[int],
                 opponent_min: int,
                 opponent_max: int):
        self.win_counter = WinCounter(player_levels, opponent_min, opponent_max)
        self.result_queue: Queue = Queue()
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.load_history()
        self.has_reported = False
        self.game_name = game_name
        if controller is not None:
            self.game_name = controller.game.name
            game_thread = Process(target=run_games,
                                  args=(controller,
                                        self.result_queue,
                                        WinCounter(source=self.win_counter)),
                                  daemon=True)
            game_thread.start()
        sn.set()
        self.artists: typing.List[plt.Artist] = []
        self.plot_lines: typing.List[plt.Line2D] = []
        self.create_plot()
        plt.tight_layout()

    def update(self, _frame):
        messages = []
        try:
            for _ in range(1000):
                messages.append(self.result_queue.get_nowait())
        except Empty:
            pass
        # logger.debug('Plotter.update() found %d messages.', len(messages))
        if not messages:
            return
        for p1_iterations, p2_iterations, result in messages:
            match_up: MatchUp = self.win_counter[(p1_iterations, p2_iterations)]
            match_up.record_result(result)
        self.write_history()

        self.artists.clear()

        self.create_plot()
        # logger.debug('Plotter.update() done.')
        return self.artists

    def create_plot(self):
        opponent_levels = self.win_counter.opponent_levels
        all_series = self.win_counter.build_series()
        total_games = sum(match_up.count for match_up in self.win_counter.values())
        self.artists.append(plt.title(
            f'Win Rates After {total_games} '
            f'Games of {self.game_name}'))
        if not self.has_reported:
            print(self.win_counter.build_summary(), end='')
            self.has_reported = True
        if not self.plot_lines:
            plt.ylabel(f'Win and tie rates')
            plt.xlabel('Opponent MCTS simulation count')
            plt.xscale('log')
            plt.ylim(0, 1)
            for name, rates in all_series:
                line, = plt.plot(opponent_levels, rates, label=name)
                self.plot_lines.append(
                    line)
            plt.legend()
        else:
            for line, (name, rates) in zip(self.plot_lines, all_series):
                # noinspection PyTypeChecker
                line.set_ydata(rates)
        self.artists.extend(self.plot_lines)

    def load_history(self):
        try:
            self.conn.execute("""\
CREATE
TABLE   games
        (
        strength1,
        strength2,
        wins1,
        ties,
        wins2
        );
""")
        except OperationalError:
            # Table already exists.
            pass
        cursor = self.conn.execute("""\
SELECT  strength1,
        strength2,
        wins1,
        ties,
        wins2
FROM    games;""")
        while True:
            rows = cursor.fetchmany()
            if not rows:
                break
            for strength1, strength2, wins1, ties, wins2 in rows:
                match_up: MatchUp = self.win_counter.get((strength1,
                                                          strength2))
                if match_up is not None:
                    match_up.p1_wins = wins1
                    match_up.ties = ties
                    match_up.p2_wins = wins2
                if strength1 != strength2:
                    match_up: MatchUp = self.win_counter.get((strength2,
                                                              strength1))
                    if match_up is not None:
                        match_up.p1_wins = wins2
                        match_up.ties = ties
                        match_up.p2_wins = wins1

    def write_history(self):
        for match_up in self.win_counter.values():
            update_count = self.conn.execute(
                """\
UPDATE  games
SET     wins1 = ?,
        ties = ?,
        wins2 = ?
WHERE   strength1 = ?
AND     strength2 = ?;
""",
                [match_up.p1_wins,
                 match_up.ties,
                 match_up.p2_wins,
                 match_up.p1_iterations,
                 match_up.p2_iterations]).rowcount
            if update_count == 0:
                self.conn.execute(
                    """\
INSERT
INTO    games
        (
        strength1,
        strength2,
        wins1,
        ties,
        wins2
        )
        VALUES
        (
        ?,
        ?,
        ?,
        ?,
        ?
        )
""",
                    [match_up.p1_iterations,
                     match_up.p2_iterations,
                     match_up.p1_wins,
                     match_up.ties,
                     match_up.p2_wins])
            self.conn.commit()


def run_games(controller: PlayController,
              result_queue: Queue,
              win_counter: WinCounter):
    player1: MctsPlayer = controller.players[Game.X_PLAYER]
    player2: MctsPlayer = controller.players[Game.O_PLAYER]

    while True:
        match_up = win_counter.find_next_matchup()
        player1.iteration_count = match_up.p1_iterations
        player2.iteration_count = match_up.p2_iterations
        # logger.debug(f'checking params {i}, {j} ({x}, {y}) with {counts[i, j]} counts')
        controller.start_game()
        while not controller.take_turn():
            pass

        result = controller.game.get_winner(controller.board)

        logger.debug('Result of pitting %d vs %d: %s.',
                     player1.iteration_count,
                     player2.iteration_count,
                     result)
        result_queue.put((player1.iteration_count,
                          player2.iteration_count,
                          result))
        match_up.record_result(result)


def create_parser(subparsers):
    parser: CommandParser = subparsers.add_parser(
        'plot',
        description='Plot player strengths.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.set_defaults(handle=handle, parser=parser)
    parser.add_argument('game',
                        default='tictactoe',
                        help='the game to play',
                        action='entry_point')
    parser.add_argument('--player_iterations',
                        nargs='*',
                        help='list of search iterations to plot for the player',
                        type=int,
                        default=[8, 64, 512])
    parser.add_argument('--opponent_min',
                        help='minimum search iterations for the opponent',
                        type=int,
                        default=1)
    parser.add_argument('--opponent_max',
                        help='minimum search iterations for the opponent',
                        type=int,
                        default=512)


def handle(args: Namespace):
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s[%(levelname)s]:%(name)s:%(message)s")
    logger.setLevel(logging.DEBUG)

    parser = args.parser
    parser.add_argument(
        '-p', '--player',
        default='mcts',
        nargs='*',
        help="the player to use",
        action='entry_point')
    args.player = ['mcts']
    args.mcts_iterations = MctsPlayer.DEFAULT_ITERATIONS

    if '__live_coding_context__' in locals():
        controller = None
    else:
        controller = PlayController(args)

    figure = plt.figure()
    db_path = os.path.abspath(os.path.join(
        __file__,
        f'../../../data/{args.game}-strengths.db'))
    logger.debug(db_path)
    plotter = Plotter(db_path,
                      args.game,
                      controller,
                      args.player_iterations,
                      args.opponent_min,
                      args.opponent_max)
    # noinspection PyUnusedLocal
    animation = FuncAnimation(figure, plotter.update, interval=30000)
    plt.show()
