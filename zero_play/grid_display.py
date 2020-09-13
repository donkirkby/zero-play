import itertools
import math
import typing

from PySide2.QtGui import QColor, QBrush, QFont, QResizeEvent
from PySide2.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, \
    QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent

from zero_play.game_state import GridGameState, GameState
from zero_play.game_display import GameDisplay, center_text_item


class GraphicsPieceItem(QGraphicsEllipseItem):
    def __init__(self, row, column, hover_listener):
        super().__init__(0, 0, 1, 1)
        self.row = row
        self.column = column
        self.setAcceptHoverEvents(True)
        self.hover_listener = hover_listener

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverEnterEvent(event)
        self.hover_listener.on_hover_enter(self)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverLeaveEvent(event)
        self.hover_listener.on_hover_leave(self)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)
        self.hover_listener.on_click(self)


class GridDisplay(GameDisplay):
    background_colour = QColor.fromRgb(0x009E0B)
    line_colour = QColor.fromRgb(0x000000)
    player1_colour = QColor.fromRgb(0x000000)
    player2_colour = QColor.fromRgb(0xFFFFFF)

    def __init__(self,
                 start_state: GridGameState):
        super().__init__(start_state)
        self.start_state: GridGameState = start_state
        self.spaces = []  # self.spaces[i][j] holds row i, column j
        self.column_dividers = []
        self.row_dividers = []
        self.column_labels = []
        self.row_labels = []
        self.text_x = self.text_y = 0

        scene = self.scene()
        scene.setBackgroundBrush(self.background_colour)
        for _ in range(start_state.board_height - 1):
            self.row_dividers.append(scene.addLine(0, 0, 1, 1))
        for _ in range(start_state.board_width - 1):
            self.column_dividers.append(scene.addLine(0, 0, 1, 1))
        for i in range(start_state.board_height):
            self.row_labels.append(scene.addSimpleText(f'{i + 1}'))
        for j in range(start_state.board_width):
            self.column_labels.append(scene.addSimpleText(chr(65+j)))
        self.to_move = scene.addEllipse(
            0, 0, 1, 1, brush=self.get_player_brush(self.start_state.X_PLAYER))
        self.move_text = scene.addSimpleText(self.choose_active_text())
        for i in range(self.start_state.board_height):
            row: typing.List[QGraphicsItem] = []
            self.spaces.append(row)
            for j in range(self.start_state.board_width):
                piece = GraphicsPieceItem(i, j, self)
                scene.addItem(piece)
                piece.setBrush(self.background_colour)
                piece.setPen(self.background_colour)
                row.append(piece)
        self.debug_message = ''

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        view_size = event.size()
        width = view_size.width()
        height = view_size.height()
        extra_columns = math.ceil(self.start_state.board_width / 6)
        margin = 1 if self.show_coordinates else 0
        cell_size = min(width // (self.start_state.board_width + extra_columns + margin),
                        height // (self.start_state.board_height + margin))
        size = cell_size*self.start_state.board_width
        x0 = (width - cell_size * (self.start_state.board_width + extra_columns + margin)) // 2
        y0 = (height - cell_size * (self.start_state.board_height + margin)) // 2
        x0 += margin*cell_size
        y0 += margin*cell_size
        font = QFont(self.default_font)
        font_size = max(1, int(cell_size // 2))
        font.setPointSize(font_size)
        for i in range(self.start_state.board_height - 1):
            r = cell_size * (i+1)
            self.row_dividers[i].setLine(x0, y0+r, x0+size, y0+r)
        for i in range(self.start_state.board_width - 1):
            r = cell_size * (i+1)
            self.column_dividers[i].setLine(x0+r, y0, x0+r, y0+size)
        for i, label in enumerate(self.row_labels):
            r = cell_size * (2*i + 1) // 2
            label.setFont(font)
            center_text_item(label, x0 - cell_size // 2, y0 + r)
        for i, label in enumerate(self.column_labels):
            r = cell_size * (2*i + 1) // 2
            label.setFont(font)
            center_text_item(label, x0 + r, y0 - cell_size // 2)
        self.to_move.setRect(x0 + size + cell_size * extra_columns // 8,
                             y0 + cell_size * self.start_state.board_height // 2 -
                             cell_size * extra_columns * 7 // 8,
                             cell_size * extra_columns * 3 // 4,
                             cell_size * extra_columns * 3 // 4)
        font_size = max(1, int(cell_size * extra_columns // 6))
        font.setPointSize(font_size)
        self.move_text.setFont(font)
        self.text_x = x0 + size + cell_size * extra_columns // 2
        self.text_y = (y0 + cell_size * self.start_state.board_height // 2 +
                       cell_size * extra_columns // 5)
        self.update_move_text()

        for i, row in enumerate(self.spaces):
            for j, piece in enumerate(row):
                x = x0 + j * cell_size + cell_size // 8
                y = y0 + i * cell_size + cell_size // 8
                piece.setRect(x, y, cell_size * 3 // 4, cell_size * 3 // 4)

    def update_board(self, state: GameState):
        assert isinstance(state, GridGameState)
        self.current_state = state
        self.valid_moves = self.current_state.get_valid_moves()
        is_ended = self.current_state.is_ended()
        spaces = self.current_state.get_spaces()
        for i in range(self.current_state.board_height):
            for j in range(self.current_state.board_width):
                player = spaces[i][j]
                piece = self.spaces[i][j]
                if player == self.current_state.NO_PLAYER:
                    if is_ended:
                        piece.setVisible(False)
                    else:
                        piece.setVisible(True)
                        piece.setBrush(self.background_colour)
                        piece.setPen(self.background_colour)
                else:
                    piece.setVisible(True)
                    piece.setBrush(self.get_player_brush(player))
                    piece.setPen(self.line_colour)
                piece.setOpacity(1)
        self.to_move.setVisible(True)
        for label in itertools.chain(self.row_labels, self.column_labels):
            label.setVisible(self.show_coordinates)
        if is_ended:
            if self.current_state.is_win(self.current_state.X_PLAYER):
                self.update_move_text('wins')
                self.to_move.setBrush(self.get_player_brush(self.current_state.X_PLAYER))
            elif self.current_state.is_win(self.current_state.O_PLAYER):
                self.update_move_text('wins')
                self.to_move.setBrush(self.get_player_brush(self.current_state.O_PLAYER))
            else:
                self.update_move_text('draw')
                self.to_move.setVisible(False)
        else:
            self.update_move_text(self.choose_active_text())
            active_player = self.current_state.get_active_player()
            self.to_move.setBrush(self.get_player_brush(active_player))

    def get_player_brush(self, player):
        return QBrush(self.player1_colour
                      if player == self.start_state.X_PLAYER
                      else self.player2_colour)

    def update_move_text(self, text: str = None):
        if self.debug_message:
            self.move_text.setText(self.debug_message)
        elif text is not None:
            self.move_text.setText(text)
        center_text_item(self.move_text, self.text_x, self.text_y)

    def on_hover_enter(self, piece_item: GraphicsPieceItem):
        if self.is_piece_played(piece_item):
            return
        active_player = self.current_state.get_active_player()
        if active_player in self.mcts_workers:
            return
        move = self.calculate_move(piece_item.row, piece_item.column)
        is_valid = self.valid_moves[move]
        if not is_valid:
            return
        piece_item.setBrush(self.get_player_brush(active_player))
        piece_item.setPen(self.line_colour)
        piece_item.setOpacity(0.5)

    def on_hover_leave(self, piece_item: GraphicsPieceItem):
        if self.is_piece_played(piece_item):
            return
        piece_item.setBrush(self.background_colour)
        piece_item.setPen(self.background_colour)
        piece_item.setOpacity(1)

    def on_click(self, piece_item: GraphicsPieceItem):
        move = self.calculate_move(piece_item.row, piece_item.column)
        is_valid = self.valid_moves[move]
        if is_valid:
            self.make_move(move)

    def calculate_move(self, row, column):
        move = row * self.start_state.board_width + column
        return move

    def is_piece_played(self, piece_item):
        current_spaces = self.current_state.get_spaces()
        hovered_player = current_spaces[piece_item.row][piece_item.column]
        return hovered_player != self.start_state.NO_PLAYER
