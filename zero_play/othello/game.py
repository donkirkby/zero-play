import typing
from copy import copy

import numpy as np

from zero_play.game_state import GridGameState


class OthelloState(GridGameState):
    game_name = 'Othello'

    def __init__(self,
                 text: str | None = None,
                 board_height: int = 6,
                 board_width: int = 6):
        if text is None:
            lines = None
            next_player_line = None
        else:
            lines = text.splitlines()
            next_player_line = lines.pop()
        super().__init__(board_height,
                         board_width,
                         lines=lines)
        spaces = self.spaces
        if text:
            assert next_player_line and next_player_line.startswith('>')
            self.active_player = (self.X_PLAYER
                                  if next_player_line.endswith('X')
                                  else self.O_PLAYER)
        else:
            self.active_player = self.X_PLAYER
            for i in range(self.board_height//2-1, self.board_height//2+1):
                for j in range(self.board_width//2-1, self.board_width//2+1):
                    player = self.X_PLAYER if (i+j) % 2 else self.O_PLAYER
                    piece_type = self.piece_types.index(player)
                    spaces[piece_type, i, j] = 1
            self.spaces = spaces

    def __eq__(self, other):
        return super().__eq__(other) and self.active_player == other.active_player

    def get_valid_moves(self) -> np.ndarray:
        spaces = self.get_spaces()
        moves = np.zeros(self.board_height * self.board_width + 1, bool)
        move_spaces = moves[:-1].reshape(self.board_width, self.board_height)
        player = self.get_active_player()
        piece_type = self.piece_types.index(player)
        for i, j in self.find_moves(spaces, piece_type):
            move_spaces[i, j] = True

        if moves.sum() == 0:
            # No moves for this player, check opponent.
            for _ in self.find_moves(spaces, 1-piece_type):
                # Opponent has a move, pass is allowed.
                moves[-1] = True
                break

        return moves

    def find_moves(self, spaces: np.ndarray, piece_type: int):
        for i in range(self.board_height):
            for j in range(self.board_width):
                if spaces[piece_type, i, j]:
                    yield from self.find_moves_from_space(spaces,
                                                          i,
                                                          j,
                                                          piece_type)

    def find_moves_from_space(self, spaces, start_row, start_column, piece_type):
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if not (di or dj):
                    continue
                has_flipped = False
                i = start_row + di
                j = start_column + dj
                while 0 <= i < self.board_height and 0 <= j < self.board_width:
                    if spaces[piece_type, i, j]:
                        break
                    if not spaces[1-piece_type, i, j]:
                        # empty space
                        if has_flipped:
                            yield i, j
                        break
                    else:
                        has_flipped = True
                    i += di
                    j += dj

    def display(self, show_coordinates: bool = False) -> str:
        result = super().display(show_coordinates)
        next_player = self.active_player
        return result + f'>{self.DISPLAY_CHARS[next_player+1]}\n'

    def display_move(self, move: int) -> str:
        if move == self.board_width * self.board_height:
            return 'PASS'
        return super().display_move(move)

    def parse_move(self, text: str) -> int:
        trimmed = text.strip().replace(' ', '')
        if not trimmed:
            return self.board_height*self.board_width  # It's a pass.
        return super().parse_move(trimmed)

    def make_move(self, move: int) -> 'OthelloState':
        new_state = copy(self)
        new_state.active_player = -self.active_player

        if move == self.board_width * self.board_height:
            return new_state  # It's a pass.

        spaces = new_state.spaces
        start_row = move // self.board_width
        start_column = move % self.board_width
        piece_type = self.piece_types.index(self.active_player)
        opponent_piece_type = 1 - piece_type
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if not (di or dj):
                    continue
                to_flip: typing.List[typing.Tuple[int, int]] = []  # [(i, j)]
                i = start_row + di
                j = start_column + dj
                while 0 <= i < self.board_height and 0 <= j < self.board_width:
                    if spaces[piece_type, i, j]:
                        for i2, j2 in to_flip:
                            spaces[opponent_piece_type, i2, j2] = 0
                            spaces[piece_type, i2, j2] = 1
                        break
                    elif not spaces[opponent_piece_type, i, j]:
                        # empty space
                        break
                    else:
                        to_flip.append((i, j))
                    i += di
                    j += dj
        spaces[piece_type, start_row, start_column] = 1
        new_state.spaces = spaces
        return new_state

    def get_active_player(self):
        return self.active_player

    def is_ended(self):
        spaces = self.spaces
        piece_type = self.piece_types.index(self.active_player)
        for _ in self.find_moves(spaces, piece_type):
            # Player has a move, not ended.
            return False
        for _ in self.find_moves(spaces, 1-piece_type):
            # Opponent has a move, not ended.
            return False
        return True

    def get_winner(self):
        if not self.is_ended():
            return self.NO_PLAYER
        spaces = self.spaces
        x_total = spaces[0].sum()
        o_total = spaces[1].sum()
        if x_total > o_total:
            return self.X_PLAYER
        if x_total < o_total:
            return self.O_PLAYER
        return self.NO_PLAYER

    def is_win(self, player: int) -> bool:
        return self.get_winner() == player
