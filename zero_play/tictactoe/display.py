import typing

from zero_play.grid_display import GridDisplay
from zero_play.tictactoe.state import TicTacToeState


class TicTacToeDisplay(GridDisplay):
    def __init__(self):
        super().__init__(TicTacToeState())

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Tic Tac Toe Game:', 'Traditional'),
                ('Tic Tac Toe Implementation:', 'Don Kirkby')]
