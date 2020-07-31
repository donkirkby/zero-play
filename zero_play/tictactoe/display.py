import typing

import numpy as np
from PySide2.QtGui import QColor, QBrush
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem

from zero_play.tictactoe.game import TicTacToeGame


class GridDisplay:
    background_colour = QColor.fromRgb(0x009E0B)
    player1_colour = QColor.fromRgb(0x000000)
    player2_colour = QColor.fromRgb(0xFFFFFF)


class TicTacToeDisplay(GridDisplay):
    def __init__(self, scene: QGraphicsScene):
        self.scene = scene
        self.game = TicTacToeGame()
        self.spaces = []

        width = scene.width()
        height = scene.height()
        cell_size = min(width//4, height//3)
        size = cell_size*3
        x0 = (width-cell_size*4) // 2
        y0 = (height-cell_size*3) // 2

        scene.setBackgroundBrush(QBrush(self.background_colour))
        for r in (cell_size, cell_size*2):
            scene.addLine(x0, y0+r, x0+size, y0+r)
            scene.addLine(x0+r, y0, x0+r, y0+size)
        self.to_move = scene.addEllipse(x0 + size * 25 // 24,
                                        y0 + size * 5 // 24,
                                        size // 4,
                                        size // 4,
                                        brush=self.get_player_brush(
                                            self.game.X_PLAYER))
        text_item = scene.addText('to move')
        font = text_item.font()
        font.setPointSize(int(size//16))
        text_item.setFont(font)
        text_item.adjustSize()
        text_rect = text_item.boundingRect()
        text_item.setPos(x0+size+cell_size//2 - text_rect.width()//2,
                         y0+size*27//48 - text_rect.height()//2)
        for i in range(self.game.board_height):
            row: typing.List[QGraphicsItem] = []
            self.spaces.append(row)
            for j in range(self.game.board_width):
                x = x0 + j * size // 3 + size // 24
                y = y0 + i * size // 3 + size // 24
                piece = scene.addEllipse(x, y, size // 4, size // 4)
                piece.setVisible(False)
                row.append(piece)

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
