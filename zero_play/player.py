import typing
from abc import ABCMeta, abstractmethod

from zero_play.game_state import GameState
from zero_play.heuristic import Heuristic
from zero_play.playout import Playout


def get_player_argument(values: typing.Sequence, player_number: int):
    """ Get the right argument for a player from a list of values.

    If there's only one value, then both players get it.
    """
    if player_number == GameState.X_PLAYER:
        i = 0
    else:
        i = -1
    return values[i]


class Player(metaclass=ABCMeta):
    def __init__(self,
                 player_number: int = GameState.X_PLAYER,
                 heuristic: Heuristic | None = None):
        if heuristic is None:
            heuristic = Playout()
        self.player_number = player_number
        self.heuristic = heuristic

    @property
    def heuristic(self):
        return self._heuristic

    @heuristic.setter
    def heuristic(self, value):
        self._heuristic = value

    @abstractmethod
    def choose_move(self, game_state: GameState) -> int:
        """ Choose a move for the given board.

        :param game_state: the current state of the game.
        :return: the chosen move's index in the list of valid moves.
        """

    def end_game(self, game_state: GameState, opponent: 'Player'):
        """ Finish a game.

        An optional method to do any needed clean up after a start_state.
        :param game_state: the current state of the game.
        :param opponent: the opposing player.
        """

    @abstractmethod
    def get_summary(self) -> typing.Sequence[str]:
        """ Human-readable attributes to describe this player. """
