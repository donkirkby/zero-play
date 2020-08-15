from zero_play.grid_display import GridDisplay
from zero_play.tictactoe.game import TicTacToeGame


class TicTacToeDisplay(GridDisplay):
    def __init__(self):
        super().__init__(TicTacToeGame())
