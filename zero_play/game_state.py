import typing
from abc import ABC, abstractmethod
from io import StringIO

import numpy as np


class GameState(ABC):
    DISPLAY_CHARS = 'O.X'
    NO_PLAYER = 0
    X_PLAYER = 1
    O_PLAYER = -1

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @property
    @abstractmethod
    def game_name(self) -> str:
        """ Display name for the game. """

    @abstractmethod
    def __eq__(self, other) -> bool:
        """ Compare with another game state. """

    @abstractmethod
    def get_valid_moves(self) -> np.ndarray:
        """ Decide which moves are valid for this board state.

        :return: an array with one boolean entry for every possible game move.
            True if that move is allowed, otherwise False. Each move's index is
            the move value to pass to make_move().
        """

    def is_ended(self) -> bool:
        """ Has the game ended in the given board? """
        if self.get_winner() != self.NO_PLAYER:
            return True
        valid_moves = self.get_valid_moves()
        return not valid_moves.any()

    @abstractmethod
    def display(self, show_coordinates: bool = False) -> str:
        """ Create human-readable display text for this board state.

        :param show_coordinates: True if the display should include coordinate
            labels.
        :return: display text. Typically, this should be valid text for passing
            to create_board().
        """

    @abstractmethod
    def display_move(self, move: int) -> str:
        """ Create human-readable display text for the given move.

        :param move: the move to describe.
        :return: display text. Typically, this should be valid text for passing
            to parse_move().
        """

    @abstractmethod
    def get_move_count(self) -> int:
        """ The number of moves that have already been made in the game. """

    @abstractmethod
    def get_spaces(self) -> np.ndarray:
        """ Extract the board spaces from the complete game state.

        Useful for teaching machine learning models.
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

    def get_active_player(self) -> int:
        """ Decide which player will play next.

        This default implementation assumes that PLAYER_X goes first, and
        the players alternate turns adding a piece to the board.
        :return: the player number to play next, typically PLAYER_X or
            PLAYER_O.
        """
        board = self.get_spaces()
        x_count = (board == self.X_PLAYER).sum()
        y_count = (board == self.O_PLAYER).sum()
        return self.X_PLAYER if x_count == y_count else self.O_PLAYER

    @abstractmethod
    def make_move(self, move: int) -> 'GameState':
        """ Get the board state after making a move.
        
        :param move: the index of a move in the result of get_valid_moves().
        :return: an array of piece values, updated by the move.
        """

    def get_winner(self) -> int:
        """ Decide which player has won, if any.
        
        :return: the player number of the winner, or NO_PLAYER if neither has
            won.
        """
        for player in (self.X_PLAYER, self.O_PLAYER):
            if self.is_win(player):
                return player

        return self.NO_PLAYER

    @abstractmethod
    def is_win(self, player: int) -> bool:
        """ Check if the given player has won on this board state.

        :param player: the player number to check.
        :return: True if the player has won.
        """


# noinspection PyAbstractClass
class GridGameState(GameState):
    def __init__(self,
                 board_height: int,
                 board_width: int,
                 text: str = None,
                 lines: typing.Sequence[str] = None,
                 spaces: np.ndarray = None,
                 extra_count: int = 0):
        self.board_height = board_height
        self.board_width = board_width
        if spaces is None:
            self.board = np.zeros(self.board_height*self.board_width + extra_count,
                                  dtype=int)
        else:
            self.board = spaces
        spaces = self.get_spaces()
        if extra_count == 0:
            self.board = spaces
        if text:
            lines = text.splitlines()
        if lines:
            if len(lines) == self.board_height + 1:
                # Trim off coordinates.
                lines = lines[1:]
                lines = [line[2:] for line in lines]
            for i, line in enumerate(lines):
                spaces[i] = [self.DISPLAY_CHARS.index(c) - 1 for c in line]

    def __repr__(self):
        board_repr = " ".join(repr(self.board).split())
        board_repr = board_repr.replace('[ ', '[')
        return f'{self.__class__.__name__}(spaces={board_repr})'

    def __eq__(self, other):
        if not isinstance(other, GridGameState):
            return False
        return np.array_equal(self.board, other.board)

    def get_move_count(self) -> int:
        return (self.get_spaces() != GameState.NO_PLAYER).sum()

    def get_spaces(self) -> np.ndarray:
        return self.board[:self.board_height*self.board_width].reshape(
            self.board_height,
            self.board_width)

    def get_valid_moves(self) -> np.ndarray:
        spaces = self.get_spaces()
        if (self.is_win(self.X_PLAYER) or
                self.is_win(self.O_PLAYER)):
            return np.zeros(self.board_height*self.board_width, bool)
        return spaces.reshape(self.board_height *
                              self.board_width) == GameState.NO_PLAYER

    def display(self, show_coordinates: bool = False) -> str:
        result = StringIO()
        if show_coordinates:
            result.write('  ')
            for i in range(65, 65+self.board_width):
                result.write(chr(i))
            result.write('\n')
        spaces = self.get_spaces()
        for i in range(self.board_height):
            if show_coordinates:
                result.write(chr(49+i) + ' ')
            for j in range(self.board_width):
                result.write(self.DISPLAY_CHARS[spaces[i, j]+1])
            result.write('\n')
        return result.getvalue()

    def display_move(self, move: int) -> str:
        row = move // self.board_width
        column = move % self.board_width
        column_text = chr(65 + column)
        return f'{row+1}{column_text}'

    def parse_move(self, text: str) -> int:
        trimmed = text.strip().replace(' ', '')
        if len(trimmed) != 2:
            raise ValueError('A move must be a row and a column.')
        row, column = trimmed[0], trimmed[1:]
        i = ord(row) - 49
        j = ord(column.upper()) - 65
        if i < 0 or self.board_height <= i:
            raise ValueError(f'Row must be between 1 and {self.board_height}.')
        if j < 0 or self.board_width <= j:
            max_column = chr(64 + self.board_width)
            raise ValueError(f'Column must be between A and {max_column}.')

        return i*self.board_width + j

    def make_move(self, move: int) -> 'GridGameState':
        moving_player = self.get_active_player()
        new_board: np.ndarray = self.board.copy()
        i, j = move // self.board_width, move % self.board_width
        new_board[i, j] = moving_player

        return self.__class__(board_height=self.board_height,
                              board_width=self.board_width,
                              spaces=new_board)
