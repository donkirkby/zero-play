import typing

from PySide2.QtWidgets import QGraphicsScene

from zero_play.grid_display import GridDisplay
from zero_play.mcts_player import MctsPlayer
from zero_play.tictactoe.game import TicTacToeGame


class TicTacToeDisplay(GridDisplay):
    def __init__(self, scene: QGraphicsScene,
                 mcts_players: typing.Sequence[MctsPlayer] = ()):
        super().__init__(scene, TicTacToeGame(), mcts_players)
