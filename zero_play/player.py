import typing
from abc import ABCMeta, abstractmethod

import numpy as np

from zero_play.game import Game
from zero_play.heuristic import Heuristic
from zero_play.playout import Playout


def get_player_argument(values: typing.Sequence, player_number: int):
    """ Get the right argument for a player from a list of values.

    If there's only one value, then both players get it.
    """
    if player_number == Game.X_PLAYER:
        i = 0
    else:
        i = -1
    return values[i]


class Player(metaclass=ABCMeta):
    def __init__(self, game: Game,
                 player_number: int = Game.X_PLAYER,
                 heuristic: typing.List[Heuristic] = None):
        if heuristic is None:
            heuristic = [Playout(game)]
        self.game = game
        self.player_number = player_number
        self.heuristic = get_player_argument(heuristic, player_number)

    @property
    def heuristic(self):
        return self._heuristic

    @heuristic.setter
    def heuristic(self, value):
        self._heuristic = value

    @abstractmethod
    def choose_move(self, board: np.ndarray) -> int:
        """ Choose a move for the given board.

        :param board: an array of piece values, like the ones returned by
            game.create_board().
        :return: the chosen move's index in the list of valid moves.
        """

    def end_game(self, board: np.ndarray, opponent: 'Player'):
        """ Finish a game.

        An optional method to do any needed clean up after a game.
        :param board: an array of piece values, representing the final game
            state.
        :param opponent: the opposing player.
        """

    @abstractmethod
    def get_summary(self) -> typing.Sequence[str]:
        """ Human-readable attributes to describe this player. """
