import typing

import numpy as np
from PySide2.QtCore import QSize
from PySide2.QtGui import QColor, QBrush, QFont
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, \
    QGraphicsSimpleTextItem, QGraphicsEllipseItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent

from zero_play.tictactoe.game import TicTacToeGame


def center_text_item(item: QGraphicsSimpleTextItem, x: float, y: float):
    bounds = item.boundingRect()
    x -= bounds.width() / 2
    y -= bounds.height() / 2
    item.setPos(x, y)


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


class GridDisplay:
    background_colour = QColor.fromRgb(0x009E0B)
    line_colour = QColor.fromRgb(0x000000)
    player1_colour = QColor.fromRgb(0x000000)
    player2_colour = QColor.fromRgb(0xFFFFFF)
    default_font = 'Sans Serif,9,-1,5,50,0,0,0,0,0'


class TicTacToeDisplay(GridDisplay):
    def __init__(self, scene: QGraphicsScene):
        self.scene = scene
        self.game = TicTacToeGame()
        self.spaces = []
        self.column_dividers = []
        self.row_dividers = []
        self.current_board = self.game.create_board()
        self.text_x = self.text_y = 0

        scene.setBackgroundBrush(self.background_colour)
        for i in range(2):
            self.row_dividers.append(scene.addLine(0, 0, 1, 1))
            self.column_dividers.append(scene.addLine(0, 0, 1, 1))
        self.to_move = scene.addEllipse(
            0, 0, 1, 1, brush=self.get_player_brush(self.game.X_PLAYER))
        self.move_text = scene.addSimpleText('to move')
        for i in range(self.game.board_height):
            row: typing.List[QGraphicsItem] = []
            self.spaces.append(row)
            for j in range(self.game.board_width):
                piece = GraphicsPieceItem(i, j, self)
                scene.addItem(piece)
                piece.setBrush(self.background_colour)
                piece.setPen(self.background_colour)
                row.append(piece)

        if scene.width() > 1:
            self.resize(scene.sceneRect().size())

    def resize(self, view_size: QSize):
        width = view_size.width()
        height = view_size.height()
        cell_size = min(width//4, height//3)
        size = cell_size*3
        x0 = (width-cell_size*4) // 2
        y0 = (height-cell_size*3) // 2
        for i in range(2):
            r = cell_size * (i+1)
            self.row_dividers[i].setLine(x0, y0+r, x0+size, y0+r)
            self.column_dividers[i].setLine(x0+r, y0, x0+r, y0+size)
        self.to_move.setRect(x0 + size * 25 // 24,
                             y0 + size * 5 // 24,
                             size // 4,
                             size // 4)
        font = QFont(self.default_font)
        font.setPointSize(int(size//18))
        self.move_text.setFont(font)
        self.text_x = x0 + size + cell_size // 2
        self.text_y = y0 + size * 27 // 48
        self.update_move_text()

        for i, row in enumerate(self.spaces):
            for j, piece in enumerate(row):
                x = x0 + j * size // 3 + size // 24
                y = y0 + i * size // 3 + size // 24
                piece.setRect(x, y, size // 4, size // 4)

    def update(self, board: np.ndarray):
        self.current_board = board
        is_ended = self.game.is_ended(board)
        spaces = self.game.get_spaces(board)
        for i in range(self.game.board_height):
            for j in range(self.game.board_width):
                player = spaces[i][j]
                piece = self.spaces[i][j]
                if player == self.game.NO_PLAYER:
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
        if is_ended:
            if self.game.is_win(board, self.game.X_PLAYER):
                self.update_move_text('wins')
                self.to_move.setBrush(self.get_player_brush(self.game.X_PLAYER))
            elif self.game.is_win(board, self.game.O_PLAYER):
                self.update_move_text('wins')
                self.to_move.setBrush(self.get_player_brush(self.game.O_PLAYER))
            else:
                self.update_move_text('draw')
                self.to_move.setVisible(False)
        else:
            self.update_move_text('to move')
            active_player = self.game.get_active_player(board)
            self.to_move.setBrush(self.get_player_brush(active_player))

    def update_move_text(self, text: str = None):
        if text is not None:
            self.move_text.setText(text)
        center_text_item(self.move_text, self.text_x, self.text_y)

    def on_hover_enter(self, piece_item: GraphicsPieceItem):
        if self.is_piece_played(piece_item):
            return
        active_player = self.game.get_active_player(self.current_board)
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
        move = piece_item.row * 3 + piece_item.column
        self.current_board = self.game.make_move(self.current_board, move)
        self.update(self.current_board)

    def is_piece_played(self, piece_item):
        current_spaces = self.game.get_spaces(self.current_board)
        hovered_player = current_spaces[piece_item.row][piece_item.column]
        return hovered_player != self.game.NO_PLAYER

    def get_player_brush(self, player):
        return QBrush(self.player1_colour
                      if player == self.game.X_PLAYER
                      else self.player2_colour)
