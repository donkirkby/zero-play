import typing

from zero_play.game_state import GameState
from zero_play.grid_display import GridDisplay
from zero_play.othello.game import OthelloState


class OthelloDisplay(GridDisplay):
    def __init__(self, board_height: int = 8, board_width: int = 8):
        super().__init__(OthelloState(board_height=board_height,
                                      board_width=board_width))
        self.ui.black_count_pixmap.setPixmap(self.player1_icon)
        self.ui.white_count_pixmap.setPixmap(self.player2_icon)
        self.update_count_text()

    # noinspection DuplicatedCode
    def update_count_text(self):
        assert isinstance(self.current_state, OthelloState)
        spaces = self.current_state.spaces
        black_count = spaces[0].sum()
        white_count = spaces[1].sum()
        self.ui.black_count.setText(f'{black_count}')
        self.ui.white_count.setText(f'{white_count}')

    def update_board(self, state: GameState):
        super().update_board(state)
        self.update_count_text()

    def get_forced_move(self):
        pass_move = len(self.valid_moves) - 1
        if self.valid_moves[pass_move]:
            return pass_move

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Othello Game:', 'Goro Hasegawa'),
                ('Othello Implementation:', 'Don Kirkby')]
