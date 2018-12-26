import numpy as np

from zero_play.tictactoe.game import TicTacToeGame


class HumanPlayer:
    @staticmethod
    def choose_move(game: TicTacToeGame,
                    board: np.ndarray,
                    moves: np.ndarray):
        active_player = game.get_active_player(board)
        player_display = game.display_player(active_player)
        prompt = f'{player_display}: '
        while True:
            move_text = input(prompt)
            try:
                move = game.parse_move(move_text)
                if moves[move]:
                    return move
            except ValueError:
                pass
            prompt = f'{move_text} is not a valid move, choose another: '
