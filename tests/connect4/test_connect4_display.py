from PySide2.QtCore import QLine
from PySide2.QtGui import QPainter, QColor, QPen

from tests.tictactoe.test_tictactoe_display import set_font_size, draw_text, trigger_resize
from zero_play.connect4.display import Connect4Display
from zero_play.connect4.game import Connect4State
from zero_play.pixmap_differ import PixmapDiffer


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
            360,
            240,
            'connect4_pieces') as (actual, expected):
        draw_grid(expected)
        expected.setBrush(Connect4Display.player1_colour)
        expected.drawEllipse(125, 205, 30, 30)
        expected.drawEllipse(165, 205, 30, 30)
        set_font_size(expected, 13)
        draw_text(expected, 320, 136, 'to move')
        expected.setBrush(Connect4Display.player2_colour)
        expected.drawEllipse(125, 165, 30, 30)
        expected.drawEllipse(290, 50, 60, 60)

        display = Connect4Display()
        board = Connect4State('''\
.......
.......
.......
.......
...O...
...XX..
''')
        trigger_resize(display, 360, 240)
        display.update_board(board)

        display.scene().render(actual)


def test_clicked(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(
            360,
            240,
            'connect4_clicked') as (actual, expected):
        draw_grid(expected)
        expected.setBrush(Connect4Display.player1_colour)
        expected.drawEllipse(5, 205, 30, 30)
        set_font_size(expected, 13)
        draw_text(expected, 320, 136, 'to move')
        colour = QColor(Connect4Display.player2_colour)
        expected.setBrush(colour)
        expected.drawEllipse(290, 50, 60, 60)
        colour.setAlpha(127)
        expected.setBrush(colour)
        colour.setRgb(0, 0, 0, 127)
        pen = QPen(colour)
        expected.setPen(pen)
        expected.drawEllipse(5, 45, 30, 30)

        display = Connect4Display()
        trigger_resize(display, 360, 240)
        space = display.spaces[1][0]
        display.on_click(space)

        display.scene().render(actual)
