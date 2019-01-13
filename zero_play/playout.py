import typing

import numpy as np

from zero_play.heuristic import Heuristic


class Playout(Heuristic):
    def analyse(self, board: np.ndarray) -> typing.Tuple[float, np.ndarray]:
        value = self.simulate(board)
        child_predictions = self.create_even_policy(board)
        return value, child_predictions

    def simulate(self, start_board: np.ndarray):
        if self.game.is_ended(start_board):
            value, policy = self.analyse_end_game(start_board)
            return value
        valid_moves, = np.nonzero(self.game.get_valid_moves(start_board))
        move = np.random.choice(valid_moves)
        next_board = self.game.make_move(start_board, move)
        return -self.simulate(next_board)
