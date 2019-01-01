import numpy as np

from zero_play.game import Game


class Connect4Game(Game):
    name = 'Connect 4'

    def create_board(self, text: str = None) -> np.ndarray:
        board = np.zeros((6, 7), dtype=int)
        if text:
            lines = text.splitlines()
            if len(lines) == 7:
                # Trim off coordinates.
                lines = lines[1:]
            for i, line in enumerate(lines):
                for j, c in enumerate(line):
                    if c == 'X':
                        board[i, j] = 1
                    elif c == 'O':
                        board[i, j] = -1
        return board

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        # Any zero value in top row in a valid move
        return board[0] == 0

    def display(self, board: np.ndarray, show_coordinates: bool = False) -> str:
        header = '1234567\n' if show_coordinates else ''
        return header + ''.join(
            ''.join(self.DISPLAY_CHARS[board[i, j]+1]
                    for j in range(7)) + '\n'
            for i in range(6))

    def display_move(self, move: int) -> str:
        return str(move+1)

    def parse_move(self, text: str) -> int:
        move_int = int(text)
        if move_int < 1 or 7 < move_int:
            raise ValueError('Move must be between 1 and 7.')
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
            for start_column in range(column_count - win_count):
                count1 = count2 = 0
                for d in range(win_count):
                    if board[start_row + d, start_column + d] == player:
                        count1 += 1
                    if board[start_row + d, start_column + win_count - d] == player:
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
