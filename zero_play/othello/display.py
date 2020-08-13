import typing

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

    def get_forced_move(self):
        pass_move = len(self.valid_moves) - 1
        if self.valid_moves[pass_move]:
            return pass_move
