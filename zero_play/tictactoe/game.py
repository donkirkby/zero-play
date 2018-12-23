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
            for i, line in enumerate(text.splitlines()):
                for j, c in enumerate(line):
                    if c == 'X':
                        board[i, j] = 1
                    elif c == 'O':
                        board[i, j] = -1
        return board

    @staticmethod
    def get_valid_moves(board: np.ndarray) -> np.ndarray:
        return board.reshape(9) == 0

    def display(self, board: np.ndarray) -> str:
        return ''.join(''.join(self.DISPLAY_CHARS[board[i, j]+1]
                               for j in range(3)) + '\n'
                       for i in range(3))

    def make_move(self, board: np.ndarray, move: int) -> np.ndarray:
        x_count = (board == self.X_PLAYER).sum()
        y_count = (board == self.O_PLAYER).sum()
        moving_player = self.X_PLAYER if x_count == y_count else self.O_PLAYER
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
