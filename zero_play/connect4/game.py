import numpy as np

from zero_play.game import GridGame


class Connect4Game(GridGame):
    name = 'Connect 4'

    def __init__(self, board_height: int = 6, board_width: int = 7):
        super().__init__(board_height, board_width)

    def create_board(self, text: str = None) -> np.ndarray:
        if text is None:
            lines = None
        else:
            lines = text.splitlines()
            if len(lines) == self.board_height+1:
                # Trim off coordinates.
                lines = lines[1:]
        return self.create_grid_board(lines=lines)

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        # Any zero value in top row in a valid move
        return board[0] == 0

    def display(self, board: np.ndarray, show_coordinates: bool = False) -> str:
        header = '1234567\n' if show_coordinates else ''
        return header + super().display(board)

    def parse_move(self, text: str, board: np.ndarray) -> int:
        move_int = int(text)
        if move_int < 1 or self.board_width < move_int:
            raise ValueError(f'Move must be between 1 and {self.board_width}.')
        return move_int - 1

    def make_move(self, board: np.ndarray, move: int) -> np.ndarray:
        moving_player = self.get_active_player(board)
        new_board: np.ndarray = board.copy()
        available_idx, = np.where(new_board[:, move] == 0)

        new_board[available_idx[-1]][move] = moving_player
        return new_board

    def is_win(self, board: np.ndarray, player: int) -> bool:
        """ Has the given player collected four in a row in any direction? """
        row_count, column_count = board.shape
        win_count = 4
        player_pieces = board == player
        if self.is_horizontal_win(player_pieces, win_count):
            return True
        if self.is_horizontal_win(player_pieces.transpose(), win_count):
            return True
        # check two diagonal strips
        for start_row in range(row_count - win_count + 1):
            for start_column in range(column_count - win_count + 1):
                count1 = count2 = 0
                for d in range(win_count):
                    if board[start_row + d, start_column + d] == player:
                        count1 += 1
                    if board[start_row + d,
                             start_column + win_count - d - 1] == player:
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
