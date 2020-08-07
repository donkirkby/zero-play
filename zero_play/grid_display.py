import math
import typing

import numpy as np
from PySide2.QtCore import QSize, QThread, Signal, Slot, QObject
from PySide2.QtGui import QColor, QBrush, QFont
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem, QGraphicsSceneHoverEvent, \
    QGraphicsSceneMouseEvent, QGraphicsSimpleTextItem

from zero_play.game import GridGame
from zero_play.mcts_player import MctsPlayer
from zero_play.mcts_worker import MctsWorker


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


class GridDisplay(QObject):
    background_colour = QColor.fromRgb(0x009E0B)
    line_colour = QColor.fromRgb(0x000000)
    player1_colour = QColor.fromRgb(0x000000)
    player2_colour = QColor.fromRgb(0xFFFFFF)
    default_font = 'Sans Serif,9,-1,5,50,0,0,0,0,0'

    move_needed = Signal(int, np.ndarray)  # active_player, board

    def __init__(self,
                 scene: QGraphicsScene,
                 game: GridGame,
                 mcts_players: typing.Sequence[MctsPlayer] = (),
                 parent: QObject = None):
        super().__init__(parent)
        self.scene = scene
        self.game = game
        self.mcts_workers: typing.Dict[int, MctsWorker] = {
            player.player_number: MctsWorker(player)
            for player in mcts_players}
        self.spaces = []  # self.spaces[i][j] holds row i, column j
        self.column_dividers = []
        self.row_dividers = []
        self.current_board = self.game.create_board()
        self.valid_moves = self.game.get_valid_moves(self.current_board)
        self.text_x = self.text_y = 0

        if not self.mcts_workers:
            self.worker_thread = None
        else:
            self.worker_thread = QThread()
            for worker in self.mcts_workers.values():
                worker.move_chosen.connect(self.make_move)  # type: ignore
                # noinspection PyUnresolvedReferences
                self.move_needed.connect(worker.choose_move)  # type: ignore
                worker.moveToThread(self.worker_thread)
            self.worker_thread.start()

        scene.clear()
        scene.setBackgroundBrush(self.background_colour)
        for _ in range(game.board_height-1):
            self.row_dividers.append(scene.addLine(0, 0, 1, 1))
        for _ in range(game.board_width-1):
            self.column_dividers.append(scene.addLine(0, 0, 1, 1))
        self.to_move = scene.addEllipse(
            0, 0, 1, 1, brush=self.get_player_brush(self.game.X_PLAYER))
        self.move_text = scene.addSimpleText(self.choose_active_text())
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
            self.update(self.current_board)

    def choose_active_text(self):
        active_player = self.game.get_active_player(self.current_board)
        if active_player in self.mcts_workers:
            return 'thinking'
        return 'to move'

    def resize(self, view_size: QSize):
        width = view_size.width()
        height = view_size.height()
        extra_columns = math.ceil(self.game.board_width/6)
        cell_size = min(width//(self.game.board_width+extra_columns),
                        height//self.game.board_height)
        size = cell_size*self.game.board_width
        x0 = (width-cell_size*(self.game.board_width+extra_columns)) // 2
        y0 = (height-cell_size*self.game.board_height) // 2
        for i in range(self.game.board_height-1):
            r = cell_size * (i+1)
            self.row_dividers[i].setLine(x0, y0+r, x0+size, y0+r)
        for i in range(self.game.board_width-1):
            r = cell_size * (i+1)
            self.column_dividers[i].setLine(x0+r, y0, x0+r, y0+size)
        self.to_move.setRect(x0 + size + cell_size * extra_columns // 8,
                             y0 + cell_size * self.game.board_height // 2 -
                             cell_size * extra_columns * 7 // 8,
                             cell_size * extra_columns * 3 // 4,
                             cell_size * extra_columns * 3 // 4)
        font = QFont(self.default_font)
        font.setPointSize(int(cell_size * extra_columns // 6))
        self.move_text.setFont(font)
        self.text_x = x0 + size + cell_size * extra_columns // 2
        self.text_y = (y0 + cell_size * self.game.board_height // 2 +
                       cell_size * extra_columns // 5)
        self.update_move_text()

        for i, row in enumerate(self.spaces):
            for j, piece in enumerate(row):
                x = x0 + j * cell_size + cell_size // 8
                y = y0 + i * cell_size + cell_size // 8
                piece.setRect(x, y, cell_size * 3 // 4, cell_size * 3 // 4)

    def update(self, board: np.ndarray):
        self.current_board = board
        self.valid_moves = self.game.get_valid_moves(board)
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
            self.update_move_text(self.choose_active_text())
            active_player = self.game.get_active_player(board)
            self.to_move.setBrush(self.get_player_brush(active_player))

    def get_player_brush(self, player):
        return QBrush(self.player1_colour
                      if player == self.game.X_PLAYER
                      else self.player2_colour)

    def update_move_text(self, text: str = None):
        if text is not None:
            self.move_text.setText(text)
        center_text_item(self.move_text, self.text_x, self.text_y)

    def on_hover_enter(self, piece_item: GraphicsPieceItem):
        if self.is_piece_played(piece_item):
            return
        active_player = self.game.get_active_player(self.current_board)
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

    @Slot(int)  # type: ignore
    def make_move(self, move):
        self.current_board = self.game.make_move(self.current_board, move)
        self.update(self.current_board)

        self.request_move()

    def request_move(self):
        if self.game.is_ended(self.current_board):
            return
        player = self.game.get_active_player(self.current_board)
        # noinspection PyUnresolvedReferences
        self.move_needed.emit(player, self.current_board)

    def calculate_move(self, row, column):
        move = row * self.game.board_width + column
        return move

    def is_piece_played(self, piece_item):
        current_spaces = self.game.get_spaces(self.current_board)
        hovered_player = current_spaces[piece_item.row][piece_item.column]
        return hovered_player != self.game.NO_PLAYER

    def close(self):
        if self.worker_thread is not None:
            self.worker_thread.quit()
