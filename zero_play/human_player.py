import numpy as np

from zero_play.game import Game


class HumanPlayer:
    @staticmethod
    def choose_move(game: Game,
                    board: np.ndarray,
                    moves: np.ndarray) -> int:
        """ Choose a move for the given board.
        
        :param game: the game's rules and helper methods
        :param board: an array of piece values, like the ones returned by
            game.create_board().
        :param moves: an array with one boolean entry for every possible game
            move, as returned by game.get_valid_moves().
        :return: the chosen move's index in moves.
        """
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
