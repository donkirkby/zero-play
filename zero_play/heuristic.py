import typing

import numpy as np
from abc import ABCMeta, abstractmethod

from zero_play.game_state import GameState


class Heuristic(metaclass=ABCMeta):
    @abstractmethod
    def get_summary(self) -> typing.Sequence[str]:
        """ Human-readable attributes to describe this heuristic. """

    @abstractmethod
    def analyse(self, board: GameState) -> typing.Tuple[float, np.ndarray]:
        """ Analyse the value of a board position and predict a move.

        :param board: the current state of the board
        :return: the estimated value of the board for the player who made the
            last move, from -1 (loss) to 0 (draw) to +1 (win), and also a
            policy for choosing the next move: weights for each move that sum
            up to 1.0.
        """

    @staticmethod
    def create_even_policy(board: GameState) -> np.ndarray:
        """ Create an evenly distributed policy across valid moves.

        If there are no valid moves, distribute across all entries.
        """
        child_valid_flags = board.get_valid_moves()
        valid_count = child_valid_flags.sum()
        if valid_count:
            child_predictions = child_valid_flags / valid_count
        else:
            child_predictions = (child_valid_flags + 1) / child_valid_flags.size
        return child_predictions

    def analyse_end_game(self, board: GameState) -> typing.Tuple[float, np.ndarray]:
        """ Calculate the value based on the winner.

        :param board: an array of piece values, that must be in an ended game
        :return: 1 if the last player to move won the game, -1 for a loss, and
        0 for a draw, plus an evenly distributed policy (probably irrelevant)
        """
        winner = board.get_winner()
        active_player = board.get_active_player()
        previous_player = -active_player
        return winner * previous_player, self.create_even_policy(board)
