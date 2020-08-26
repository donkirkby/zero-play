import typing

from zero_play.grid_display import GridDisplay
from zero_play.tictactoe.game import TicTacToeGame


class TicTacToeDisplay(GridDisplay):
    def __init__(self):
        super().__init__(TicTacToeGame())

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Tic Tac Toe Game:', 'Traditional'),
                ('Tic Tac Toe Implementation:', 'Don Kirkby')]
