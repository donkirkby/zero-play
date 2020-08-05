from PySide2.QtWidgets import QGraphicsScene

from zero_play.grid_display import GridDisplay
from zero_play.tictactoe.game import TicTacToeGame


class TicTacToeDisplay(GridDisplay):
    def __init__(self, scene: QGraphicsScene):
        super().__init__(scene, TicTacToeGame())
