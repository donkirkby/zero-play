import typing

import numpy as np

from zero_play.game_state import GameState
from zero_play.heuristic import Heuristic


class Playout(Heuristic):
    def get_summary(self) -> typing.Sequence[str]:
        return 'playout',

    def analyse(self, board: GameState) -> typing.Tuple[float, np.ndarray]:
        value = self.simulate(board)
        child_predictions = self.create_even_policy(board)
        return value, child_predictions

    def simulate(self, start_state: GameState):
        if start_state.is_ended():
            value, policy = self.analyse_end_game(start_state)
            return value
        valid_moves, = np.nonzero(start_state.get_valid_moves())
        move = np.random.choice(valid_moves)
        new_state = start_state.make_move(move)
        return -self.simulate(new_state)
