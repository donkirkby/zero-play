from argparse import Namespace, ArgumentParser, ArgumentDefaultsHelpFormatter, ArgumentTypeError
from importlib import import_module

import numpy as np

from zero_play.human_player import HumanPlayer
from zero_play.game import Game


def parse_args():
    parser = ArgumentParser(description='Pit two players against each other.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--game',
                        default='zero_play.tictactoe.game.TicTacToeGame',
                        type=imported_argument)
    return parser.parse_args()


def imported_argument(full_class_name):
    module_name, class_name = full_class_name.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except ImportError as ex:
        raise ArgumentTypeError("can't import " + module_name) from ex
    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ArgumentTypeError("attribute {} not found on module {}".format(
            class_name,
            module_name))


class PlayController:
    def __init__(self, game_class, player1_args, player2_args):
        self.game: Game = game_class()
        self.players = {1: player1_args.player(),
                        -1: player2_args.player()}
        self.board: np.ndarray = self.game.create_board()

    def take_turn(self):
        self.display_board()
        valid_moves = self.game.get_valid_moves(self.board)
        player_number = self.game.get_active_player(self.board)
        player = self.players[player_number]
        move = player.choose_move(self.game, self.board, valid_moves)
        print()
        self.board = self.game.make_move(self.board, move)
        winner = self.game.get_winner(self.board)
        if not self.game.is_ended(self.board):
            return False

        self.display_board()
        if winner == self.game.NO_PLAYER:
            print('The game is a draw.')
        else:
            print(self.game.display_player(winner), 'Wins.')
        return True

    def display_board(self):
        print(self.game.display(self.board, show_coordinates=True), end='')


def main():
    args = parse_args()
    player1_args = player2_args = Namespace(player=HumanPlayer)
    controller = PlayController(args.game, player1_args, player2_args)
    while not controller.take_turn():
        pass


if __name__ == '__main__':
    main()
