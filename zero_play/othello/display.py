import typing

import numpy as np
from PySide2.QtWidgets import QGraphicsScene

from zero_play.game import GridGame
from zero_play.grid_display import GridDisplay
from zero_play.mcts_player import MctsPlayer


class OthelloDisplay(GridDisplay):
    def __init__(self,
                 scene: QGraphicsScene,
                 game: GridGame,
                 mcts_players: typing.Sequence[MctsPlayer] = ()):
        super().__init__(scene, game, mcts_players)

    def update(self, board: np.ndarray):
        super().update(board)
        if self.valid_moves[-1]:
            move = len(self.valid_moves) - 1
            self.make_move(move)
