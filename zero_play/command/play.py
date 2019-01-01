from argparse import Namespace, ArgumentParser, ArgumentDefaultsHelpFormatter, ArgumentTypeError
from importlib import import_module

import numpy as np

from zero_play.human_player import HumanPlayer
from zero_play.game import Game
from zero_play.mcts_player import MctsPlayer


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
        self.players = {
            Game.X_PLAYER: player1_args.player(self.game, Game.X_PLAYER),
            Game.O_PLAYER: player2_args.player(self.game, Game.O_PLAYER)}
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


def main():
    args = parse_args()
    player1_args = Namespace(player=MctsPlayer)
    player2_args = Namespace(player=HumanPlayer)
    controller = PlayController(args.game, player1_args, player2_args)
    while not controller.take_turn():
        pass


if __name__ == '__main__':
    main()
