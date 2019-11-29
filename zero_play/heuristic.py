import typing

import numpy as np
from abc import ABCMeta, abstractmethod

from zero_play.game import Game


class Heuristic(metaclass=ABCMeta):
    def __init__(self, game: Game):
        """ Initialize the heuristic object.

        Subclasses must override this if they want to report which games this
        heuristic can play.
        :param game: the game object that contains the game rules
        :raises ValueError: if the game is not one of the games this heuristic
            can play
        """
        self.game = game

    @abstractmethod
    def get_summary(self) -> typing.Sequence[str]:
        """ Human-readable attributes to describe this heuristic. """

    @abstractmethod
    def analyse(self, board: np.ndarray) -> typing.Tuple[float, np.ndarray]:
        """ Analyse the value of a board position and predict a move.

        :param board: the current state of the board
        :return: the estimated value of the board for the player who made the
            last move, from -1 (loss) to 0 (draw) to +1 (win), and also a
            policy for choosing the next move: weights for each move that sum
            up to 1.0.
        """

    def create_even_policy(self, board: np.ndarray) -> np.ndarray:
        """ Create an evenly distributed policy across valid moves.

        If there are no valid moves, distribute across all entries.
        """
        child_valid_flags = self.game.get_valid_moves(board)
        valid_count = child_valid_flags.sum()
        if valid_count:
            child_predictions = child_valid_flags / valid_count
        else:
            child_predictions = (child_valid_flags + 1) / child_valid_flags.size
        return child_predictions

    def analyse_end_game(self, board: np.ndarray) -> typing.Tuple[float, np.ndarray]:
        """ Calculate the value based on the winner.

        :param board: an array of piece values, that must be in an ended game
        :return: 1 if the last player to move won the game, -1 for a loss, and
        0 for a draw, plus an evenly distributed policy (probably irrelevant)
        """
        winner = self.game.get_winner(board)
        active_player = self.game.get_active_player(board)
        previous_player = -active_player
        return winner * previous_player, self.create_even_policy(board)
