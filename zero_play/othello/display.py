import typing

from PySide2.QtGui import QResizeEvent

from zero_play.game_display import center_text_item
from zero_play.game_state import GameState
from zero_play.grid_display import GridDisplay
from zero_play.othello.game import OthelloState


class OthelloDisplay(GridDisplay):
    def __init__(self, board_height: int = 8, board_width: int = 8):
        super().__init__(OthelloState(board_height=board_height,
                                      board_width=board_width))
        scene = self.scene()
        black_pen = self.get_player_brush(self.start_state.X_PLAYER)
        white_pen = self.get_player_brush(self.start_state.O_PLAYER)
        self.small_black_item = scene.addEllipse(0, 0,
                                                 1, 1,
                                                 brush=black_pen)
        self.small_white_item = scene.addEllipse(0, 0,
                                                 1, 1,
                                                 brush=white_pen)
        self.black_count = scene.addSimpleText('0')
        self.white_count = scene.addSimpleText('0')
        self.black_count_x = self.white_count_x = self.count_y = 0

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        x0 = round(self.row_dividers[0].boundingRect().x())
        y0 = round(self.column_dividers[0].boundingRect().y())
        grid_size = self.row_dividers[0].boundingRect().width()
        small_size = grid_size * 9//200
        self.small_black_item.setRect(x0 + grid_size * 212//200,
                                      y0 + grid_size * 25//200,
                                      small_size, small_size)
        self.small_white_item.setRect(x0 + grid_size * 229//200,
                                      y0 + grid_size * 25//200,
                                      small_size, small_size)

        self.count_y = y0 + grid_size*42//200
        self.black_count_x = x0 + grid_size*217//200
        self.white_count_x = x0 + grid_size*234//200
        font = self.move_text.font()
        self.black_count.setFont(font)
        self.white_count.setFont(font)
        self.update_count_text()

    # noinspection DuplicatedCode
    def update_count_text(self):
        assert isinstance(self.current_state, OthelloState)
        black_count = self.current_state.get_piece_count(
            self.current_state.X_PLAYER)
        white_count = self.current_state.get_piece_count(
            self.current_state.O_PLAYER)
        self.black_count.setText(f'{black_count}')
        self.white_count.setText(f'{white_count}')
        center_text_item(self.black_count, self.black_count_x, self.count_y)
        center_text_item(self.white_count, self.white_count_x, self.count_y)

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
