import math
import typing
from abc import ABC, abstractmethod

import numpy as np


class GameState(ABC):
    DISPLAY_CHARS = 'O.X'
    NO_PLAYER = 0
    X_PLAYER = 1
    O_PLAYER = -1
    players = (X_PLAYER, O_PLAYER)

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

    def get_players(self) -> typing.Iterable[int]:
        return self.X_PLAYER, self.O_PLAYER

    @abstractmethod
    def get_move_count(self) -> int:
        """ The number of moves that have already been made in the game. """

    @property
    @abstractmethod
    def spaces(self) -> np.ndarray:
        """ Extract the board spaces from the complete game state.

        Useful for teaching machine learning models.
        """

    @spaces.setter
    @abstractmethod
    def spaces(self, spaces: np.ndarray):
        """ Set pieces on the board spaces. """

    def get_spaces(self) -> np.ndarray:
        return self.spaces

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
        x_count = board[0].sum()
        y_count = board[1].sum()
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
    """ Game state for a simple grid with pieces on it. """
    def __init__(self,
                 board_height: int,
                 board_width: int,
                 text: str | None = None,
                 lines: typing.Sequence[str] | None = None,
                 spaces: np.ndarray | None = None):
        """ Initialize a new instance.

        :param board_height: number of rows in the grid
        :param board_width: number of columns in the grid
        :param text: text representation of the game state, like that returned
            by display()
        :param lines: equivalent to text, but already split into lines
        :param spaces: 3-dimensional boolean array 1 when a piece type is
            in a grid space, 0 when it isn't, with shape
            (piece_type_count, board_height, board_width)
        """
        self.board_height = board_height
        self.board_width = board_width
        if spaces is not None:
            assert text is None
            assert lines is None
            self.spaces = spaces
            return
        type_count = len(self.piece_types)
        packed = np.zeros(math.ceil(board_height*board_width*type_count/8),
                          dtype=np.uint8)
        self.packed = packed
        if text:
            lines = text.splitlines()
        if lines:
            if len(lines) == self.board_height + 1:
                # Trim off coordinates.
                lines = lines[1:]
                lines = [line[2:] for line in lines]
            line_array = np.array(lines, dtype=str)
            chars = line_array.view('U1').reshape(self.board_height,
                                                  self.board_width)
            spaces = self.get_spaces()
            for layer, display_char in enumerate(self.piece_displays):
                spaces[layer] = chars == display_char
        if spaces is not None:
            self.spaces = spaces

    def __repr__(self):
        board_text = self.display()
        return f'{self.__class__.__name__}({board_text!r})'

    def __eq__(self, other):
        if not isinstance(other, GridGameState):
            return False
        return np.array_equal(self.spaces, other.spaces)

    @property
    def piece_types(self):
        return self.X_PLAYER, self.O_PLAYER

    @property
    def piece_displays(self):
        return 'XO'

    def get_move_count(self) -> int:
        return self.spaces.sum()

    @property
    def spaces(self) -> np.ndarray:
        type_count = len(self.piece_types)
        trimmed_size = self.board_height * self.board_width * type_count
        trimmed = np.unpackbits(self.packed)[:trimmed_size]
        return trimmed.reshape(type_count,
                               self.board_height,
                               self.board_width)

    @spaces.setter
    def spaces(self, spaces):
        self.packed = np.packbits(spaces)

    def get_valid_moves(self) -> np.ndarray:
        spaces = self.get_spaces()
        full_spaces = np.logical_or.accumulate(spaces)[-1]
        empty_spaces = np.logical_not(full_spaces)
        return empty_spaces.reshape(self.board_height * self.board_width)

    def display(self, show_coordinates: bool = False) -> str:
        spaces = self.get_spaces().astype(bool)
        display_grid = np.full((self.board_height, self.board_width), '.')
        for level, char in enumerate(self.piece_displays):
            np.copyto(display_grid, char, where=spaces[level])
        lines = np.full(self.board_height, '')
        if show_coordinates:
            lines = np.char.add(lines,
                                [chr(49+i) + ' '
                                 for i in range(self.board_height)])
        for j in range(self.board_width):
            lines = np.char.add(lines, display_grid[:, j])
        text = '\n'.join(lines) + '\n'
        if show_coordinates:
            header = '  ' + ''.join(chr(i)
                                    for i in range(65, 65 + self.board_width))
            text = header + '\n' + text
        return text

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
        piece_type = self.piece_types.index(moving_player)
        new_spaces = self.get_spaces()  # always an unpacked copy
        i, j = move // self.board_width, move % self.board_width
        new_spaces[piece_type, i, j] = 1

        return self.__class__(board_height=self.board_height,
                              board_width=self.board_width,
                              spaces=new_spaces)
