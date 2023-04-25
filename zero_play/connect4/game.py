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
        return self.board[0] == 0

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
        new_board: np.ndarray = self.board.copy()
        available_idx, = np.where(new_board[:, move] == 0)

        new_board[available_idx[-1]][move] = moving_player
        return Connect4State(spaces=new_board)

    def is_win(self, player: int) -> bool:
        """ Has the given player collected four in a row in any direction? """
        row_count, column_count = self.board.shape
        win_count = 4
        player_pieces = self.board == player
        if self.is_horizontal_win(player_pieces, win_count):
            return True
        if self.is_horizontal_win(player_pieces.transpose(), win_count):
            return True
        # check two diagonal strips
        for start_row in range(row_count - win_count + 1):
            for start_column in range(column_count - win_count + 1):
                count1 = count2 = 0
                for d in range(win_count):
                    if self.board[start_row + d, start_column + d] == player:
                        count1 += 1
                    if self.board[start_row + d,
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
