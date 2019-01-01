import typing
from argparse import Namespace, ArgumentParser, ArgumentDefaultsHelpFormatter

import numpy as np

from zero_play.human_player import HumanPlayer
from zero_play.game import Game
from zero_play.mcts_player import MctsPlayer


def parse_args():
    parser = ArgumentParser(description='Pit two players against each other.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    Game.add_argument(parser)
    return parser.parse_args()


class PlayController:
    def __init__(self, game_class: typing.Type[Game], player1_args, player2_args):
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
    game_class = Game.load(args.game)
    player1_args = Namespace(player=MctsPlayer)
    player2_args = Namespace(player=HumanPlayer)
    controller = PlayController(game_class, player1_args, player2_args)
    while not controller.take_turn():
        pass


if __name__ == '__main__':
    main()
