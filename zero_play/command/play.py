from argparse import Namespace

import numpy as np

from zero_play.human_player import HumanPlayer
from zero_play.tictactoe.game import TicTacToeGame


class PlayController:
    def __init__(self, game_class, player1_args, player2_args):
        self.game: TicTacToeGame = game_class()
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
        if winner == self.game.NO_PLAYER:
            return False

        self.display_board()
        print(self.game.display_player(winner), 'Wins.')
        return True

    def display_board(self):
        print(self.game.display(self.board, show_coordinates=True), end='')


def main():
    player1_args = player2_args = Namespace(player=HumanPlayer)
    controller = PlayController(TicTacToeGame, player1_args, player2_args)
    while not controller.take_turn():
        pass


if __name__ == '__main__':
    main()
