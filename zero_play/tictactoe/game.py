import numpy as np


class TicTacToeGame:
    DISPLAY_CHARS = 'O.X'
    NO_PLAYER = 0
    X_PLAYER = 1
    O_PLAYER = -1

    @staticmethod
    def create_board(text: str = None) -> np.ndarray:
        board = np.zeros((3, 3), dtype=int)
        if text:
            lines = text.splitlines()
            if len(lines) == 4:
                # Trim off coordinates.
                lines = lines[1:]
                lines = [line[2:] for line in lines]
            for i, line in enumerate(lines):
                for j, c in enumerate(line):
                    if c == 'X':
                        board[i, j] = 1
                    elif c == 'O':
                        board[i, j] = -1
        return board

    @staticmethod
    def get_valid_moves(board: np.ndarray) -> np.ndarray:
        return board.reshape(9) == 0

    def display(self, board: np.ndarray, show_coordinates: bool = False) -> str:
        size = 3
        header = '  ABC\n' if show_coordinates else ''
        row_headers = [str(i+1) + ' ' if show_coordinates else ''
                       for i in range(size)]
        return header + ''.join(
            row_headers[i] + ''.join(self.DISPLAY_CHARS[board[i, j]+1]
                                     for j in range(3)) + '\n'
            for i in range(3))

    @staticmethod
    def display_move(move: int) -> str:
        size = 3
        i, j = move // size, move % size
        return f'{i+1}{chr(j+65)}'

    @staticmethod
    def parse_move(text: str) -> int:
        size = 3
        clean_text = text.upper().strip()
        if len(clean_text) != 2:
            raise ValueError('Move must have one number and one letter.')
        y, x = map(ord, clean_text)
        i, j = y-49, x-65
        if i >= size:
            raise ValueError(f'Row must be between 1 and {size}.')
        if j >= size:
            raise ValueError(f'Column must be between A and {chr(64+size)}.')
        return i*size + j

    def display_player(self, player: int) -> str:
        if player == self.X_PLAYER:
            return 'Player X'
        return 'Player O'

    def get_active_player(self, board: np.ndarray) -> int:
        x_count = (board == self.X_PLAYER).sum()
        y_count = (board == self.O_PLAYER).sum()
        return self.X_PLAYER if x_count == y_count else self.O_PLAYER

    def make_move(self, board: np.ndarray, move: int) -> np.ndarray:
        moving_player = self.get_active_player(board)
        new_board: np.ndarray = board.copy()
        i, j = move // 3, move % 3
        new_board[i, j] = moving_player
        return new_board

    def get_winner(self, board: np.ndarray) -> int:
        for player in (self.X_PLAYER, self.O_PLAYER):
            if self.is_win(board, player):
                return player

        return self.NO_PLAYER

    @staticmethod
    def is_win(board: np.ndarray, player: int) -> bool:
        """ Has the given player collected a triplet in any direction? """
        size = 3
        # check horizontal lines
        for i in range(size):
            count = 0
            for j in range(size):
                if board[i, j] == player:
                    count += 1
            if count == size:
                return True
        # check vertical lines
        for j in range(size):
            count = 0
            for i in range(size):
                if board[i, j] == player:
                    count += 1
            if count == size:
                return True
        # check two diagonal strips
        count1 = count2 = 0
        for d in range(size):
            if board[d, d] == player:
                count1 += 1
            if board[d, size-d-1] == player:
                count2 += 1
        if count1 == size or count2 == size:
            return True

        return False
