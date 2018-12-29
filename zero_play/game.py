import typing
from abc import ABC, abstractmethod

import numpy as np


class Game(ABC):
    DISPLAY_CHARS = 'O.X'
    NO_PLAYER = 0
    X_PLAYER = 1
    O_PLAYER = -1

    def __repr__(self):
        return f"{self.__class__.__name__}()"

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
    
    @staticmethod
    def create_hashable_board(board: np.ndarray) -> typing.Hashable:
        """ Create a hashable representation for a game board.
        
        :param board: an array of piece values, like the ones returned by
            create_board().
        :return: a hashable representation of board.
        """
        powers = np.arange(board.size).reshape(board.shape)
        coefficients = 3 ** powers
        piece_values = 1 + board
        terms = piece_values * coefficients
        h = terms.sum()
        return int(h)

    def parse_hashable_board(self,
                             hashable_board: typing.Hashable) -> np.ndarray:
        """ Parse a hashable board back into an array of piece values.

        :param hashable_board: a hashable representation of a board.
        :return: an array of piece values, like the ones returned by
            create_board().
        """
        if not isinstance(hashable_board, int):
            raise NotImplementedError(
                'Override this method to support other hashable board types.')
        board = self.create_board()
        row_count, column_count = board.shape
        for space_index in range(board.size):
            piece_value = (hashable_board % 3) - 1
            i = space_index // column_count
            j = space_index % column_count
            board[i, j] = piece_value
            hashable_board //= 3
        return board

    @abstractmethod
    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        """ Decide which moves are valid for the given board.

        :param board: an array of piece values, like the ones returned by
            create_board().
        :return: an array with one boolean entry for every possible game move.
            True if that move is allowed from the given board, otherwise
            False. Each move's index is the move value to pass to make_move()
            or display_move().
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
    def display_move(self, move: int) -> str:
        """ Create human-readable display text for the given move.

        :param move: the index of a move in the result of get_valid_moves().
        :return: display text. Typically, this should be the coordinates, and
            it should be valid text for passing to parse_move().
        """

    @abstractmethod
    def parse_move(self, text: str) -> int:
        """ Parse a human-readable description into a move index.

        :param text: the move description, typically coordinates
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
