from copy import copy

import numpy as np

from zero_play.game_state import GridGameState


class Connect4State(GridGameState):
    game_name = 'Connect 4'

    def __init__(self,
                 text: str | None = None,
                 board_height: int = 6,
                 board_width: int = 7,
                 spaces: np.ndarray | None = None):
        if text is None:
            lines = None
        else:
            lines = text.splitlines()
            if len(lines) == board_height+1:
                # Trim off coordinates.
                lines = lines[1:]
        super().__init__(board_height, board_width, lines=lines, spaces=spaces)

    def get_valid_moves(self) -> np.ndarray:
        if self.get_winner() != self.NO_PLAYER:
            return np.zeros(self.board_width, dtype=bool)
        # Any zero value in top row is a valid move
        return self.spaces[:, 0].sum(axis=0) == 0

    def display(self, show_coordinates: bool = False) -> str:
        header = '1234567\n' if show_coordinates else ''
        return header + super().display()

    def parse_move(self, text: str) -> int:
        move_int = int(text)
        if move_int < 1 or self.board_width < move_int:
            raise ValueError(f'Move must be between 1 and {self.board_width}.')
        return move_int - 1

    def make_move(self, move: int) -> 'Connect4State':
        moving_player = self.get_active_player()
        new_board = copy(self)
        spaces = new_board.spaces
        empty_spaces = spaces.sum(axis=0) == 0
        available_idx, = np.where(empty_spaces[:, move])

        piece_type = self.piece_types.index(moving_player)
        spaces[piece_type, available_idx[-1], move] = 1
        new_board.spaces = spaces
        return new_board

    def is_win(self, player: int) -> bool:
        """ Has the given player collected four in a row in any direction? """
        row_count, column_count = self.board_height, self.board_width
        win_count = 4
        spaces = self.spaces
        piece_type = self.piece_types.index(player)
        player_pieces = spaces[piece_type]
        if self.is_horizontal_win(player_pieces, win_count):
            return True
        if self.is_horizontal_win(player_pieces.transpose(), win_count):
            return True
        # check two diagonal strips
        for start_row in range(row_count - win_count + 1):
            for start_column in range(column_count - win_count + 1):
                count1 = count2 = 0
                for d in range(win_count):
                    if player_pieces[start_row + d, start_column + d]:
                        count1 += 1
                    if player_pieces[start_row + d,
                                     start_column + win_count - d - 1]:
                        count2 += 1
                if count1 == win_count or count2 == win_count:
                    return True

        return False

    @staticmethod
    def is_horizontal_win(player_pieces: np.ndarray, win_count):
        row_count, column_count = player_pieces.shape
        for i in range(row_count):
            for j in range(column_count-win_count+1):
                count = player_pieces[i, j:j+win_count].sum()
                if count >= win_count:
                    return True
        return False
