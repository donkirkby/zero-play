import typing
from PySide2.QtWidgets import QGraphicsScene

from zero_play.grid_display import GridDisplay, GraphicsPieceItem
from zero_play.connect4.game import Connect4Game
from zero_play.mcts_player import MctsPlayer


class Connect4Display(GridDisplay):
    def __init__(self, scene: QGraphicsScene,
                 mcts_players: typing.Sequence[MctsPlayer] = ()):
        super().__init__(scene, Connect4Game(), mcts_players)

    def calculate_move(self, row, column):
        return column

    def on_click(self, piece_item: GraphicsPieceItem):
        super().on_click(piece_item)
        # Display a preview of the move, if it's still available.
        self.on_hover_enter(piece_item)
