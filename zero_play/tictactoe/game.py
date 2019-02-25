import numpy as np

from zero_play.game import GridGame


class TicTacToeGame(GridGame):
    name = 'Tic Tac Toe'

    def __init__(self):
        super().__init__(board_height=3, board_width=3)

    def is_win(self, board: np.ndarray, player: int) -> bool:
        """ Has the given player collected a triplet in any direction? """
        size = self.board_width
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
