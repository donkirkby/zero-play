import typing
from argparse import Namespace, ArgumentDefaultsHelpFormatter
from csv import DictWriter
from datetime import datetime

import numpy as np

from zero_play.game import Game
from zero_play.command_parser import CommandParser
from zero_play.mcts_player import MctsPlayer
from zero_play.player import Player, get_player_argument


def load_arguments(args: Namespace) -> typing.Tuple[Game, typing.List[Player]]:
    parser: CommandParser = args.parser
    game: Game = parser.load_argument(args, 'game')
    heuristics = [parser.load_argument(args,
                                       'heuristic',
                                       get_player_argument(args.heuristic,
                                                           Game.X_PLAYER),
                                       game=game),
                  parser.load_argument(args,
                                       'heuristic',
                                       get_player_argument(args.heuristic,
                                                           Game.O_PLAYER),
                                       game=game)]
    player_names = args.player
    players = [parser.load_argument(args,
                                    'player',
                                    get_player_argument(player_names,
                                                        Game.X_PLAYER),
                                    game=game,
                                    player_number=Game.X_PLAYER,
                                    heuristic=heuristics),
               parser.load_argument(
                                    args,
                                    'player',
                                    get_player_argument(player_names,
                                                        Game.O_PLAYER),
                                    game=game,
                                    player_number=Game.O_PLAYER,
                                    heuristic=heuristics)]
    return game, players


class PlayController:
    def __init__(self, game: Game, players: typing.List[Player]):
        self.game = game
        x_player, o_player = players
        x_player.player_number = game.X_PLAYER
        o_player.player_number = game.O_PLAYER
        self.players = {Game.X_PLAYER: x_player, Game.O_PLAYER: o_player}
        self.board: typing.Optional[np.ndarray] = None
        self.start_game()

    def start_game(self):
        self.board = self.game.create_board()

    def take_turn(self) -> bool:
        """ Take one turn in the game, and return True if the game is over. """
        player_number = self.game.get_active_player(self.board)
        player = self.players[player_number]
        move = player.choose_move(self.board)
        self.board = self.game.make_move(self.board, move)
        if not self.game.is_ended(self.board):
            return False

        other_player = self.players[-player_number]
        player.end_game(self.board, other_player)
        other_player.end_game(self.board, player)

        return True

    def play(self, games: int = 1, flip: bool = False, display: bool = False):
        current_x = original_x = self.players[self.game.X_PLAYER]
        current_o = original_o = self.players[self.game.O_PLAYER]
        wins = {original_x: 0,
                original_o: 0}
        ties = 0
        for i in range(games):
            if i and flip:
                current_x = self.players[self.game.O_PLAYER]
                current_o = self.players[self.game.X_PLAYER]
                current_x.player_number = self.game.X_PLAYER
                current_o.player_number = self.game.O_PLAYER
                self.players[self.game.X_PLAYER] = current_x
                self.players[self.game.O_PLAYER] = current_o
            while True:
                if display:
                    print(self.game.display(self.board, show_coordinates=True))
                if self.take_turn():
                    break
            if display:
                print(self.game.display(self.board, show_coordinates=True))
            if self.game.is_win(self.board, self.game.X_PLAYER):
                wins[current_x] += 1
            elif self.game.is_win(self.board, self.game.O_PLAYER):
                wins[current_o] += 1
            else:
                ties += 1
            self.start_game()
        original_x.player_number = self.game.X_PLAYER
        original_o.player_number = self.game.O_PLAYER
        self.players[self.game.X_PLAYER] = original_x
        self.players[self.game.O_PLAYER] = original_o
        if display:
            print(get_result_summary(original_x,
                                     original_o,
                                     wins[original_x],
                                     ties,
                                     wins[original_o]),
                  end='')

        return wins[original_x], ties, wins[original_o]


def get_result_summary(player_a, player_b, wins_a, ties, wins_b):
    player_summaries = get_player_summaries(player_a, player_b)
    return f"""\
{wins_a} wins for {player_summaries[0]}
{ties} ties
{wins_b} wins for {player_summaries[1]}
"""


def get_player_summaries(*players: Player) -> typing.Sequence[str]:
    summaries = [player.get_summary() for player in players]
    for category_values in zip(*summaries):
        if len(set(category_values)) > 1:
            return category_values
    return 'player A', 'player B'


def create_parser(subparsers):
    parser: CommandParser = subparsers.add_parser(
        'play',
        description='Pit two players against each other.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.set_defaults(handle=handle, parser=parser)
    parser.add_argument('game',
                        default='tictactoe',
                        help='the game to play',
                        action='entry_point')
    parser.add_argument(
        '-p', '--players',
        default=['human', 'mcts'],
        nargs='*',
        help="the player to use, pass two names if they're different",
        action='entry_point',
        dest='player')
    parser.add_argument('--heuristic',
                        default=['playout'],
                        nargs='*',
                        help='heuristic for evaluating boards',
                        action='entry_point')
    parser.add_argument('--display',
                        action='store_true',
                        help='display moves')
    parser.add_argument('--num_games',
                        '-n',
                        type=int,
                        default=1,
                        help='number of games to play')
    parser.add_argument('--flip',
                        action='store_true',
                        help='flip first player back and forth each game')


def handle(args: Namespace):
    game, players = load_arguments(args)
    players[0].heuristic.load_checkpoint('data/connect4-nn', filename='best.h5')
    players[1].heuristic.load_checkpoint('data/connect4-nn',
                                         filename=f'checkpoint-01.h5')
    controller = PlayController(game, players)
    base_player = MctsPlayer(game, iteration_count=args.mcts_iterations)
    base_controller = PlayController(game, [players[0], base_player])
    with open('data/connect4-comparison.csv', 'w') as f:
        writer = DictWriter(f, ['wins_vs_best',
                                'ties_vs_best',
                                'losses_vs_best',
                                'wins_vs_base',
                                'ties_vs_base',
                                'losses_vs_base',
                                'time'])
        writer.writeheader()
        while True:
            wins, ties, losses = controller.play(games=2,
                                                 flip=True)
            wins_vs_base, ties_vs_base, losses_vs_base = base_controller.play(
                games=2,
                flip=True)
            now = datetime.now()
            writer.writerow(dict(wins_vs_best=wins,
                                 ties_vs_best=ties,
                                 losses_vs_best=losses,
                                 wins_vs_base=wins_vs_base,
                                 ties_vs_base=ties_vs_base,
                                 losses_vs_base=losses_vs_base,
                                 time=now.strftime('%Y-%m-%d %H:%M:%S')))
            f.flush()
