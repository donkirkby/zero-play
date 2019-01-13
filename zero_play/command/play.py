import typing
from argparse import ArgumentDefaultsHelpFormatter, Namespace

import numpy as np

from zero_play.game import Game
from zero_play.zero_play import CommandParser


class PlayController:
    def __init__(self, parser: CommandParser, args: Namespace = None):
        if args is None:
            args = parser.parse_args()
        self.game: Game = parser.load_argument(args, 'game')
        player_names = args.player
        self.players = {
            Game.X_PLAYER: parser.load_argument(
                args,
                'player',
                get_player_argument(player_names, Game.X_PLAYER),
                game=self.game,
                player_number=Game.X_PLAYER),
            Game.O_PLAYER: parser.load_argument(
                args,
                'player',
                get_player_argument(player_names, Game.O_PLAYER),
                game=self.game,
                player_number=Game.O_PLAYER)}
        self.board: np.ndarray = None
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


def create_parser():
    parser = CommandParser(description='Pit two players against each other.',
                           formatter_class=ArgumentDefaultsHelpFormatter)
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
    return parser


def get_player_argument(values: typing.Sequence, player_number: int):
    """ Get the right argument for a player from a list of values.

    If there's only one value, then both players get it.
    """
    if player_number == Game.X_PLAYER:
        i = 0
    else:
        i = -1
    return values[i]


def main():
    parser = create_parser()
    args = parser.parse_args()
    controller = PlayController(parser, args)
    while not controller.take_turn():
        pass


if __name__ == '__main__':
    main()
