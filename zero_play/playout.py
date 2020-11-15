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

    def simulate(self, start_state: GameState) -> float:
        """ Simulate the rest of a game by choosing random moves.

        :param start_state: the game state to start the simulation at
        :return: 1 if the start_state's active player won the game, -1 for a
            loss, and 0 for a draw
        """
        current_state = start_state
        multiplier = 1
        while True:
            if current_state.is_ended():
                value, policy = self.analyse_end_game(current_state)
                return multiplier*value
            valid_moves, = np.nonzero(current_state.get_valid_moves())
            if len(valid_moves) == 0:
                raise ValueError('No valid moves found.\n' + current_state.display())
            move = np.random.choice(valid_moves)
            new_state = current_state.make_move(move)
            if new_state.get_active_player() != current_state.get_active_player():
                multiplier *= -1
            current_state = new_state
