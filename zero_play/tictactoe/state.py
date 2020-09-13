import numpy as np

from zero_play.game_state import GridGameState


class TicTacToeState(GridGameState):
    game_name = 'Tic Tac Toe'

    def __init__(self,
                 text: str = None,
                 spaces: np.ndarray = None,
                 board_height: int = 3,
                 board_width: int = 3):
        super().__init__(board_height=board_height,
                         board_width=board_width,
                         text=text,
                         spaces=spaces)

    def is_win(self, player: int) -> bool:
        """ Has the given player collected a triplet in any direction? """
        size = self.board_width
        spaces = self.get_spaces()
        # check horizontal lines
        for i in range(size):
            count = 0
            for j in range(size):
                if spaces[i, j] == player:
                    count += 1
            if count == size:
                return True
        # check vertical lines
        for j in range(size):
            count = 0
            for i in range(size):
                if spaces[i, j] == player:
                    count += 1
            if count == size:
                return True
        # check two diagonal strips
        count1 = count2 = 0
        for d in range(size):
            if spaces[d, d] == player:
                count1 += 1
            if spaces[d, size-d-1] == player:
                count2 += 1
        if count1 == size or count2 == size:
            return True

        return False
