import numpy as np

from zero_play.game import Game


class HumanPlayer:
    def __init__(self, game: Game):
        self.game = game

    def choose_move(self, board: np.ndarray) -> int:
        """ Choose a move for the given board.
        
        :param board: an array of piece values, like the ones returned by
            game.create_board().
        :return: the chosen move's index in the list of valid moves.
        """
        moves = self.game.get_valid_moves(board)
        active_player = self.game.get_active_player(board)
        player_display = self.game.display_player(active_player)
        prompt = f'{player_display}: '
        while True:
            move_text = input(prompt)
            try:
                move = self.game.parse_move(move_text)
                if moves[move]:
                    return move
            except ValueError:
                pass
            prompt = f'{move_text} is not a valid move, choose another: '
