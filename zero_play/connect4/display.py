import typing

from zero_play.connect4.game import Connect4Game
from zero_play.grid_display import GridDisplay, GraphicsPieceItem


class Connect4Display(GridDisplay):
    def __init__(self):
        super().__init__(Connect4Game())

    def calculate_move(self, row, column):
        return column

    def on_click(self, piece_item: GraphicsPieceItem):
        super().on_click(piece_item)
        # Display a preview of the move, if it's still available.
        self.on_hover_enter(piece_item)

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [("Connect 4 / Captain's Mistress Game:", 'Traditional'),
                ('Connect 4 Implementation:', 'Don Kirkby')]
