from PySide2.QtCore import QLine
from PySide2.QtGui import QPainter, QColor, QPen

from zero_play.connect4.display import Connect4Display
from zero_play.connect4.game import Connect4State
from zero_play.pixmap_differ import PixmapDiffer, render_display


def draw_grid(expected):
    expected.fillRect(0, 0,
                      360, 240,
                      Connect4Display.background_colour)
    expected.drawLines([QLine(0, y, 280, y)
                        for y in range(40, 240, 40)])
    expected.drawLines([QLine(x, 0, x, 280)
                        for x in range(40, 280, 40)])


def test_pieces(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(
            280,
            240,
            'connect4_pieces') as (actual, expected):
        draw_grid(expected)
        expected.setBrush(Connect4Display.player1_colour)
        expected.drawEllipse(125, 205, 30, 30)
        expected.drawEllipse(165, 205, 30, 30)
        expected.setBrush(Connect4Display.player2_colour)
        expected.drawEllipse(125, 165, 30, 30)

        display = Connect4Display()
        board = Connect4State('''\
.......
.......
.......
.......
...O...
...XX..
''')
        display.resize(372, 264)
        display.update_board(board)

        render_display(display, actual)


def test_clicked(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(
            280,
            240,
            'connect4_clicked') as (actual, expected):
        draw_grid(expected)
        expected.setBrush(Connect4Display.player1_colour)
        expected.drawEllipse(5, 205, 30, 30)
        colour = QColor(Connect4Display.player2_colour)
        colour.setAlpha(127)
        expected.setBrush(colour)
        colour.setRgb(0, 0, 0, 127)
        pen = QPen(colour)
        expected.setPen(pen)
        expected.drawEllipse(5, 45, 30, 30)

        display = Connect4Display()
        display.resize(372, 264)
        display.grab()  # Force layout to recalculate.

        space = display.spaces[1][0]
        display.on_click(space)

        render_display(display, actual)
