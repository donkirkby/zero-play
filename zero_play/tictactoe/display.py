import typing

import numpy as np
from PySide2.QtCore import QSize
from PySide2.QtGui import QColor, QBrush, QFont
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, \
    QGraphicsSimpleTextItem

from zero_play.tictactoe.game import TicTacToeGame


def center_text_item(item: QGraphicsSimpleTextItem, x: float, y: float):
    bounds = item.boundingRect()
    x -= bounds.width() / 2
    y -= bounds.height() / 2
    item.setPos(x, y)


class GridDisplay:
    background_colour = QColor.fromRgb(0x009E0B)
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

        scene.setBackgroundBrush(QBrush(self.background_colour))
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
                piece = scene.addEllipse(0, 0, 1, 1)
                piece.setVisible(False)
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
        center_text_item(self.move_text, x0+size+cell_size//2, y0+size*27//48)

        for i, row in enumerate(self.spaces):
            for j, piece in enumerate(row):
                x = x0 + j * size // 3 + size // 24
                y = y0 + i * size // 3 + size // 24
                piece.setRect(x, y, size // 4, size // 4)

    def update(self, board: np.ndarray):
        spaces = self.game.get_spaces(board)
        for i in range(self.game.board_height):
            for j in range(self.game.board_width):
                player = spaces[i][j]
                if player == self.game.NO_PLAYER:
                    continue
                piece = self.spaces[i][j]
                piece.setBrush(self.get_player_brush(player))
                piece.setVisible(True)
        active_player = self.game.get_active_player(board)
        self.to_move.setBrush(self.get_player_brush(active_player))

    def get_player_brush(self, player):
        return QBrush(self.player1_colour
                      if player == self.game.X_PLAYER
                      else self.player2_colour)
