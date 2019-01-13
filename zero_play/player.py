import typing
from abc import ABCMeta, abstractmethod

import numpy as np

from zero_play.command.play import get_player_argument
from zero_play.game import Game
from zero_play.heuristic import Heuristic
from zero_play.playout import Playout


class Player(metaclass=ABCMeta):
    def __init__(self, game: Game,
                 player_number: int = Game.X_PLAYER,
                 heuristic: typing.List[Heuristic] = None):
        if heuristic is None:
            heuristic = [Playout(game)]
        self.game = game
        self.player_number = player_number
        self.heuristic = get_player_argument(heuristic, player_number)

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
