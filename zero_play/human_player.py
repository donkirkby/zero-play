import typing

import numpy as np

from zero_play.game import Game
from zero_play.player import Player


class HumanPlayer(Player):
    def choose_move(self, board: np.ndarray) -> int:
        """ Choose a move for the given board.
        
        :param board: an array of piece values, like the ones returned by
            game.create_board().
        :return: the chosen move's index in the list of valid moves.
        """
        moves = self.game.get_valid_moves(board)
        display = self.game.display(board, show_coordinates=True)
        active_player = self.game.get_active_player(board)
        player_display = self.game.display_player(active_player)
        prompt = f'{display}{player_display}: '
        while True:
            move_text = input(prompt)
            try:
                move = self.game.parse_move(move_text, board)
                if moves[move]:
                    print()
                    return move
            except ValueError:
                pass
            prompt = f'{move_text} is not a valid move, choose another: '

    def end_game(self, board: np.ndarray, opponent: Player):
        """ Finish a game.

        :param board: an array of piece values, representing the final game
            state.
        :param opponent: the opposing player.
        """
        if (not isinstance(opponent, HumanPlayer) or
                self.player_number == Game.X_PLAYER):
            print(self.game.display(board, show_coordinates=True), end='')
            winner = self.game.get_winner(board)
            if winner == self.game.NO_PLAYER:
                print('The game is a draw.')
            else:
                print(self.game.display_player(winner), 'Wins.')

    def get_summary(self) -> typing.Sequence[str]:
        return 'human',
