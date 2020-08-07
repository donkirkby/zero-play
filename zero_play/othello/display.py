import typing

import numpy as np
from PySide2.QtWidgets import QGraphicsScene

from zero_play.grid_display import GridDisplay
from zero_play.mcts_player import MctsPlayer
from zero_play.othello.game import OthelloGame


class OthelloDisplay(GridDisplay):
    def __init__(self, scene: QGraphicsScene,
                 mcts_players: typing.Sequence[MctsPlayer] = ()):
        super().__init__(scene, OthelloGame(), mcts_players)

    def update(self, board: np.ndarray):
        super().update(board)
        if self.valid_moves[-1]:
            move = len(self.valid_moves) - 1
            self.make_move(move)
