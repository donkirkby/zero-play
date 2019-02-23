from abc import ABC, abstractmethod

import numpy as np


class Game(ABC):
    DISPLAY_CHARS = 'O.X'
    NO_PLAYER = 0
    X_PLAYER = 1
    O_PLAYER = -1

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @property
    @abstractmethod
    def name(self) -> str:
        """ Display name for the game. """

    @abstractmethod
    def create_board(self, text: str = None) -> np.ndarray:
        """ Create an array of piece values for a game board.

        :param text: A text representation of the board state. Depending on the
            game, it might contain "X" for X_PLAYER, "O" for O_PLAYER, and "."
            for empty spaces. It may also contain coordinate labels, which
            should be ignored.
        :return: an array where each value is the state of one board space.
            Typical states are NO_PLAYER, X_PLAYER, and O_PLAYER.
        """

    @abstractmethod
    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        """ Decide which moves are valid for the given board.

        :param board: an array of piece values, like the ones returned by
            create_board().
        :return: an array with one boolean entry for every possible game move.
            True if that move is allowed from the given board, otherwise
            False. Each move's index is the move value to pass to make_move().
        """

    def is_ended(self, board: np.ndarray) -> bool:
        """ Has the game ended in the given board? """
        if self.get_winner(board) != self.NO_PLAYER:
            return True
        valid_moves = self.get_valid_moves(board)
        return not valid_moves.any()

    @abstractmethod
    def display(self, board: np.ndarray, show_coordinates: bool = False) -> str:
        """ Create human-readable display text for the given board.

        :param board: an array of piece values, like the ones returned by
            create_board().
        :param show_coordinates: True if the display should include coordinate
            labels.
        :return: display text. Typically, this should be valid text for passing
            to create_board().
        """

    @abstractmethod
    def get_spaces(self, board: np.ndarray) -> np.ndarray:
        """ Extract the board spaces from the complete game state. """

    @abstractmethod
    def parse_move(self, text: str, board: np.ndarray) -> int:
        """ Parse a human-readable description into a move index.

        :param text: the move description, typically coordinates
        :param board: an array of piece values, like the ones returned by
            create_board().
        :return: the index of a move in the result of get_valid_moves().
        :raise: ValueError if text is invalid.
        """

    def display_player(self, player: int) -> str:
        """ Create human-readable display text for a player. """
        if player == self.X_PLAYER:
            return 'Player X'
        return 'Player O'

    def get_active_player(self, board: np.ndarray) -> int:
        """ Decide which player will play next.

        This default implementation assumes that PLAYER_X goes first, and
        the players alternate turns adding a piece to the board.
        :param board: an array of piece values, like the ones returned by
            create_board().
        :return: the player number to play next, typically PLAYER_X or
            PLAYER_O.
        """
        x_count = (board == self.X_PLAYER).sum()
        y_count = (board == self.O_PLAYER).sum()
        return self.X_PLAYER if x_count == y_count else self.O_PLAYER

    @abstractmethod
    def make_move(self, board: np.ndarray, move: int) -> np.ndarray:
        """ Get the board state after making a move.
        
        :param board: an array of piece values, like the ones returned by
            create_board(). It is not changed by this method.
        :param move: the index of a move in the result of get_valid_moves().
        :return: an array of piece values, updated by the move.
        """

    def get_winner(self, board: np.ndarray) -> int:
        """ Decide which player has won, if any.
        
        :param board: an array of piece values, like the ones returned by
            create_board().
        :return: the player number of the winner, or NO_PLAYER if neither has
            won.
        """
        for player in (self.X_PLAYER, self.O_PLAYER):
            if self.is_win(board, player):
                return player

        return self.NO_PLAYER

    @abstractmethod
    def is_win(self, board: np.ndarray, player: int) -> bool:
        """ Check if the given player has won on the given board.

        :param board: an array of piece values, like the ones returned by
            create_board().
        :param player: the player number to check.
        :return: True if the player has won.
        """


# noinspection PyAbstractClass
class GridGame(Game):
    def __init__(self, board_height: int, board_width: int):
        super(GridGame, self).__init__()
        self.board_height = board_height
        self.board_width = board_width

    def get_spaces(self, board: np.ndarray) -> np.ndarray:
        return board[:self.board_height*self.board_width].reshape(
            self.board_height,
            self.board_width)
