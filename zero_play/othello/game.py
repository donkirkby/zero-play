import typing
from io import StringIO

import numpy as np

from zero_play.game import Game


class OthelloGame(Game):
    name = 'Othello'

    def __init__(self, board_height: int = 6, board_width: int = 6):
        super(OthelloGame, self).__init__()
        self.board_height = board_height
        self.board_width = board_width

    def create_board(self, text: str = None) -> np.ndarray:
        board = np.zeros(self.board_height*self.board_width+1, dtype=int)
        spaces = self.get_spaces(board)
        if not text:
            board[-1] = self.X_PLAYER
            for i in range(self.board_height//2-1, self.board_height//2+1):
                for j in range(self.board_width//2-1, self.board_width//2+1):
                    player = self.X_PLAYER if (i+j) % 2 else self.O_PLAYER
                    spaces[i, j] = player
        else:
            lines = text.splitlines()
            next_player_line = lines.pop()
            assert next_player_line.startswith('>')
            board[-1] = (self.X_PLAYER
                         if next_player_line.endswith('X')
                         else self.O_PLAYER)
            if len(lines) == self.board_height + 1:
                # Trim off coordinates.
                lines = [line[1:] for line in lines[1:]]
            for i, line in enumerate(lines):
                for j, c in enumerate(line):
                    if c == 'X':
                        spaces[i, j] = self.X_PLAYER
                    elif c == 'O':
                        spaces[i, j] = self.O_PLAYER
        return board

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        spaces = self.get_spaces(board)
        moves = np.zeros(self.board_height * self.board_width + 1, bool)
        move_spaces = moves[:-1].reshape(self.board_width, self.board_height)
        player = board[-1]
        for i, j in self.find_moves(spaces, player):
            move_spaces[i, j] = True

        moves[-1] = moves.sum() == 0
        return moves

    def find_moves(self, spaces: np.ndarray, player: int):
        for i in range(self.board_height):
            for j in range(self.board_width):
                piece = spaces[i, j]
                if piece == player:
                    yield from self.find_moves_from_space(spaces, i, j, player)

    def find_moves_from_space(self, spaces, start_row, start_column, player):
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if not (di or dj):
                    continue
                has_flipped = False
                i = start_row + di
                j = start_column + dj
                while 0 <= i < self.board_height and 0 <= j < self.board_width:
                    piece = spaces[i, j]
                    if piece == player:
                        break
                    if piece == self.NO_PLAYER:
                        if has_flipped:
                            yield i, j
                            break
                    else:
                        has_flipped = True
                    i += di
                    j += dj

    def display(self, board: np.ndarray, show_coordinates: bool = False) -> str:
        result = StringIO()
        if show_coordinates:
            result.write(' ')
            for i in range(65, 65+self.board_width):
                result.write(chr(i))
            result.write('\n')
        spaces = self.get_spaces(board)
        next_player = board[-1]
        for i in range(self.board_height):
            if show_coordinates:
                result.write(chr(49+i))
            for j in range(self.board_height):
                result.write(self.DISPLAY_CHARS[spaces[i, j]+1])
            result.write('\n')
        result.write(f'>{self.DISPLAY_CHARS[next_player+1]}\n')
        return result.getvalue()

    def get_spaces(self, board):
        return board[:-1].reshape(self.board_height, self.board_width)

    def parse_move(self, text: str, board: np.ndarray) -> int:
        trimmed = text.strip().replace(' ', '')
        if not trimmed:
            return self.board_height*self.board_width  # It's a pass.
        if len(trimmed) != 2:
            raise ValueError('A move must be a row and a column.')
        row, column = trimmed
        i = ord(row) - 49
        j = ord(column.upper()) - 65
        if i < 0 or self.board_height <= i:
            raise ValueError(f'Row must be between 1 and {self.board_height}.')
        if j < 0 or self.board_width <= j:
            max_column = chr(64 + self.board_width)
            raise ValueError(f'Column must be between A and {max_column}.')

        return i*self.board_width + j

    def make_move(self, board: np.ndarray, move: int) -> np.ndarray:
        new_board: np.ndarray = board.copy()
        player = new_board[-1]
        new_board[-1] = -player

        if move == self.board_width * self.board_height:
            return new_board  # It's a pass.

        spaces = self.get_spaces(new_board)
        start_row = move // self.board_width
        start_column = move % self.board_width
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if not (di or dj):
                    continue
                to_flip: typing.List[typing.Tuple[int, int]] = []  # [(i, j)]
                i = start_row + di
                j = start_column + dj
                while 0 <= i < self.board_height and 0 <= j < self.board_width:
                    piece = spaces[i, j]
                    if piece == player:
                        for i, j in to_flip:
                            spaces[i, j] *= -1
                        break
                    if piece == self.NO_PLAYER:
                        break
                    else:
                        to_flip.append((i, j))
                    i += di
                    j += dj
        spaces[start_row, start_column] = player
        return new_board

    def get_active_player(self, board: np.ndarray):
        return board[-1]

    def is_ended(self, board: np.ndarray):
        spaces = self.get_spaces(board)
        player = board[-1]
        for _ in self.find_moves(spaces, player):
            return False
        for _ in self.find_moves(spaces, -player):
            return False
        return True

    def get_winner(self, board: np.ndarray):
        if not self.is_ended(board):
            return self.NO_PLAYER
        total = board[:-1].sum()
        if total > 0:
            return self.X_PLAYER
        if total < 0:
            return self.O_PLAYER
        return self.NO_PLAYER

    def is_win(self, board: np.ndarray, player: int) -> bool:
        return self.get_winner(board) == player
