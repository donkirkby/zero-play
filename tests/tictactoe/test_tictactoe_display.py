from PySide2.QtWidgets import QGraphicsScene

# noinspection PyUnresolvedReferences
from tests.pixmap_differ import PixmapDiffer, pixmap_differ
from zero_play.tictactoe.display import TicTacToeDisplay


def draw_square_grid(expected):
    expected.fillRect(0, 0, 320, 240, TicTacToeDisplay.background_colour)
    expected.drawLine(0, 80, 240, 80)
    expected.drawLine(0, 160, 240, 160)
    expected.drawLine(80, 0, 80, 240)
    expected.drawLine(160, 0, 160, 240)


def test_start_square(pixmap_differ: PixmapDiffer):
    size = 240
    actual, expected = pixmap_differ.start(size+80, size, 'tictactoe_start_square')

    draw_square_grid(expected)
    expected.setBrush(TicTacToeDisplay.player1_colour)
    expected.drawEllipse(250, 50, 60, 60)
    print('Font:', expected.font().toString())
    set_font_size(expected, 15)
    expected.drawText(244, 143, 'to move')

    scene = QGraphicsScene(0, 0, size+80, size)
    TicTacToeDisplay(scene)

    scene.render(actual)
    pixmap_differ.assert_equal()


def test_start_wide(pixmap_differ: PixmapDiffer):
    size = 240
    actual, expected = pixmap_differ.start(size*2+80, size, 'tictactoe_start_wide')

    expected.fillRect(0, 0, size * 2 + 80, size, TicTacToeDisplay.background_colour)
    expected.drawLine(120, 80, 360, 80)
    expected.drawLine(120, 160, 360, 160)
    expected.drawLine(200, 0, 200, 240)
    expected.drawLine(280, 0, 280, 240)
    expected.setBrush(TicTacToeDisplay.player1_colour)
    expected.drawEllipse(370, 50, 60, 60)
    set_font_size(expected, 15)
    expected.drawText(364, 143, 'to move')

    scene = QGraphicsScene(0, 0, size*2 + 80, size)
    TicTacToeDisplay(scene)

    scene.render(actual)
    pixmap_differ.assert_equal()


def test_start_tall(pixmap_differ: PixmapDiffer):
    size = 120
    actual, expected = pixmap_differ.start(size + 40, size*2, 'tictactoe_start_tall')

    expected.fillRect(0, 0, size + 40, size * 2, TicTacToeDisplay.background_colour)
    expected.drawLine(0, 100, 120, 100)
    expected.drawLine(0, 140, 120, 140)
    expected.drawLine(40, 60, 40, 180)
    expected.drawLine(80, 60, 80, 180)
    expected.setBrush(TicTacToeDisplay.player1_colour)
    expected.drawEllipse(125, 85, 30, 30)
    set_font_size(expected, 7)
    expected.drawText(124, 131, 'to move')

    scene = QGraphicsScene(0, 0, size + 40, size*2)
    TicTacToeDisplay(scene)

    scene.render(actual)
    pixmap_differ.assert_equal()


def set_font_size(painter, size):
    font = painter.font()
    font.setPointSize(size)
    painter.setFont(font)


def test_pieces(pixmap_differ: PixmapDiffer):
    size = 240
    actual, expected = pixmap_differ.start(size+80, size, 'tictactoe_pieces')

    draw_square_grid(expected)
    expected.setBrush(TicTacToeDisplay.player1_colour)
    expected.drawEllipse(10, 10, 60, 60)
    expected.drawEllipse(90, 90, 60, 60)
    set_font_size(expected, 15)
    expected.drawText(244, 143, 'to move')
    expected.setBrush(TicTacToeDisplay.player2_colour)
    expected.drawEllipse(90, 10, 60, 60)
    expected.drawEllipse(250, 50, 60, 60)

    scene = QGraphicsScene(0, 0, size+80, size)
    display = TicTacToeDisplay(scene)
    board = display.game.create_board('''\
XO.
.X.
...
''')
    display.update(board)

    scene.render(actual)
    pixmap_differ.assert_equal()
