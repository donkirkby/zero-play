import typing

from zero_play.grid_display import GridDisplay
from zero_play.othello.game import OthelloGame


class OthelloDisplay(GridDisplay):
    def __init__(self, board_height: int = 8, board_width: int = 8):
        super().__init__(OthelloGame(board_height, board_width))

    def get_forced_move(self):
        pass_move = len(self.valid_moves) - 1
        if self.valid_moves[pass_move]:
            return pass_move

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Othello Game:', 'Goro Hasegawa'),
                ('Othello Implementation:', 'Don Kirkby')]
