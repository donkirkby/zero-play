import math
import typing

import numpy as np

from zero_play.game_state import GridGameState


class OthelloState(GridGameState):
    game_name = 'Othello'

    def __init__(self,
                 text: str | None = None,
                 board_height: int = 6,
                 board_width: int = 6,
                 spaces: np.ndarray | None = None):
        if spaces is not None:
            size = spaces.size
            board_width = board_height = int(math.sqrt(size-1))
            assert text is None
        if text is None:
            lines = None
            next_player_line = None
        else:
            lines = text.splitlines()
            next_player_line = lines.pop()
        super().__init__(board_height,
                         board_width,
                         lines=lines,
                         extra_count=1,
                         spaces=spaces)
        if spaces is not None:
            return
        spaces = self.get_spaces()
        if text:
            assert next_player_line and next_player_line.startswith('>')
            self.board[-1] = (self.X_PLAYER
                              if next_player_line.endswith('X')
                              else self.O_PLAYER)
        else:
            self.board[-1] = self.X_PLAYER
            for i in range(self.board_height//2-1, self.board_height//2+1):
                for j in range(self.board_width//2-1, self.board_width//2+1):
                    player = self.X_PLAYER if (i+j) % 2 else self.O_PLAYER
                    spaces[i, j] = player

    def get_valid_moves(self) -> np.ndarray:
        spaces = self.get_spaces()
        moves = np.zeros(self.board_height * self.board_width + 1, bool)
        move_spaces = moves[:-1].reshape(self.board_width, self.board_height)
        player = self.get_active_player()
        for i, j in self.find_moves(spaces, player):
            move_spaces[i, j] = True

        if moves.sum() == 0:
            # No moves for this player, check opponent.
            for _ in self.find_moves(spaces, -player):
                # Opponent has a move, pass is allowed.
                moves[-1] = True
                break

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

    def display(self, show_coordinates: bool = False) -> str:
        result = super().display(show_coordinates)
        next_player = self.board[-1]
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
        new_board: np.ndarray = self.board.copy()
        player = new_board[-1]
        new_board[-1] = -player

        new_state = OthelloState(spaces=new_board)
        if move == self.board_width * self.board_height:
            return new_state  # It's a pass.

        spaces = new_state.get_spaces()
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
        return new_state

    def get_active_player(self):
        return self.board[-1]

    def is_ended(self):
        spaces = self.get_spaces()
        player = self.board[-1]
        for _ in self.find_moves(spaces, player):
            return False
        for _ in self.find_moves(spaces, -player):
            return False
        return True

    def get_winner(self):
        if not self.is_ended():
            return self.NO_PLAYER
        total = self.board[:-1].sum()
        if total > 0:
            return self.X_PLAYER
        if total < 0:
            return self.O_PLAYER
        return self.NO_PLAYER

    def get_piece_count(self, player: int):
        return (self.board[:-1] == player).sum()

    def is_win(self, player: int) -> bool:
        return self.get_winner() == player
