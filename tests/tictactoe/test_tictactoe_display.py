from PySide2.QtCore import QSize
from PySide2.QtGui import QFont, QPainter, QColor, QPen
from PySide2.QtWidgets import QGraphicsScene

from zero_play.grid_display import center_text_item
from zero_play.mcts_player import MctsPlayer
from zero_play.pixmap_differ import PixmapDiffer
from zero_play.tictactoe.display import TicTacToeDisplay
from zero_play.tictactoe.game import TicTacToeGame


def draw_square_grid(expected):
    expected.fillRect(0, 0, 320, 240, TicTacToeDisplay.background_colour)
    expected.drawLine(0, 80, 240, 80)
    expected.drawLine(0, 160, 240, 160)
    expected.drawLine(80, 0, 80, 240)
    expected.drawLine(160, 0, 160, 240)


# noinspection DuplicatedCode
def test_start_square(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_start_square') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(250, 50, 60, 60)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'to move')

        display = TicTacToeDisplay()
        display.resize(QSize(size+80, size))

        display.scene.render(actual)


def test_start_wide(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size*2+80,
            size,
            'tictactoe_start_wide') as (actual, expected):
        expected.fillRect(0, 0, size * 2 + 80, size, TicTacToeDisplay.background_colour)
        expected.drawLine(120, 80, 360, 80)
        expected.drawLine(120, 160, 360, 160)
        expected.drawLine(200, 0, 200, 240)
        expected.drawLine(280, 0, 280, 240)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(370, 50, 60, 60)
        set_font_size(expected, 13)
        draw_text(expected, 400, 136, 'to move')

        display = TicTacToeDisplay()
        display.resize(QSize(size*2+80, size))

        display.scene.render(actual)


def test_start_tall(pixmap_differ: PixmapDiffer):
    size = 120
    with pixmap_differ.create_painters(
            size+40,
            size*2,
            'tictactoe_start_tall') as (actual, expected):
        expected.fillRect(0, 0, size + 40, size * 2, TicTacToeDisplay.background_colour)
        expected.drawLine(0, 100, 120, 100)
        expected.drawLine(0, 140, 120, 140)
        expected.drawLine(40, 60, 40, 180)
        expected.drawLine(80, 60, 80, 180)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(125, 85, 30, 30)
        set_font_size(expected, 6)
        draw_text(expected, 140, 128, 'to move')

        display = TicTacToeDisplay()
        display.resize(QSize(size+40, size*2))

        display.scene.render(actual)


def set_font_size(painter, size):
    font = QFont(TicTacToeDisplay.default_font)
    font.setPointSize(size)
    painter.setFont(font)


def draw_text(expected: QPainter, x: int, y: int, text: str):
    window = expected.window()
    scene = QGraphicsScene(0, 0, window.width(), window.height())
    text_item = scene.addSimpleText(text)
    font = expected.font()
    text_item.setFont(font)
    center_text_item(text_item, x, y)
    scene.render(expected)


def test_pieces(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_pieces') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        expected.drawEllipse(90, 90, 60, 60)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'to move')
        expected.setBrush(TicTacToeDisplay.player2_colour)
        expected.drawEllipse(90, 10, 60, 60)
        expected.drawEllipse(250, 50, 60, 60)

        display = TicTacToeDisplay()
        display.resize(QSize(size+80, size))
        board = display.game.create_board('''\
XO.
.X.
...
''')
        display.update(board)

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_piece_hover_enter(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_piece_hover_enter') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'to move')
        colour = QColor(TicTacToeDisplay.player2_colour)
        expected.setBrush(colour)
        expected.drawEllipse(250, 50, 60, 60)
        colour.setAlpha(127)
        expected.setBrush(colour)
        colour.setRgb(0, 0, 0, 127)
        pen = QPen(colour)
        expected.setPen(pen)
        expected.drawEllipse(90, 10, 60, 60)

        display = TicTacToeDisplay()
        display.resize(QSize(size+80, size))

        board = display.game.create_board('''\
X..
...
...
''')
        display.update(board)
        display.on_hover_enter(display.spaces[0][1])

        display.scene.render(actual)


def test_piece_hover_enter_mcts(pixmap_differ: PixmapDiffer):
    """ Don't display move options while MCTS player is thinking. """
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_piece_hover_enter_mcts') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'thinking')
        expected.drawEllipse(250, 50, 60, 60)

        display = TicTacToeDisplay()
        player = MctsPlayer(display.game, TicTacToeGame.X_PLAYER)
        display.mcts_players = (player, )
        display.resize(QSize(size+80, size))

        display.on_hover_enter(display.spaces[0][1])

        display.scene.render(actual)
        display.close()


# noinspection DuplicatedCode
def test_piece_hover_leave(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_piece_hover_leave') as (actual, expected):
        draw_square_grid(expected)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'to move')
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(250, 50, 60, 60)

        display = TicTacToeDisplay()
        display.resize(QSize(size+80, size))

        display.on_hover_enter(display.spaces[0][1])
        display.on_hover_leave(display.spaces[0][1])

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_piece_hover_existing(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_piece_hover_existing') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'to move')
        colour = QColor(TicTacToeDisplay.player2_colour)
        expected.setBrush(colour)
        expected.drawEllipse(250, 50, 60, 60)

        display = TicTacToeDisplay()
        display.resize(QSize(size+80, size))

        board = display.game.create_board('''\
X..
...
...
''')
        display.update(board)
        display.on_hover_enter(display.spaces[0][0])

        display.scene.render(actual)


def test_piece_click(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_piece_click') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'to move')
        expected.setBrush(TicTacToeDisplay.player2_colour)
        expected.drawEllipse(250, 50, 60, 60)

        display = TicTacToeDisplay()
        display.resize(QSize(size+80, size))

        display.on_click(display.spaces[0][0])

        display.scene.render(actual)


def test_winner(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_winner') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        expected.drawEllipse(90, 90, 60, 60)
        expected.drawEllipse(170, 170, 60, 60)
        expected.drawEllipse(250, 50, 60, 60)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'wins')
        expected.setBrush(TicTacToeDisplay.player2_colour)
        expected.drawEllipse(90, 10, 60, 60)
        expected.drawEllipse(170, 90, 60, 60)

        display = TicTacToeDisplay()
        display.resize(QSize(size+80, size))

        board = display.game.create_board('''\
XO.
.XO
..X
''')
        display.update(board)

        display.scene.render(actual)

    assert not display.spaces[0][2].isVisible()


def test_draw(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'tictactoe_draw') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        expected.drawEllipse(10, 90, 60, 60)
        expected.drawEllipse(90, 170, 60, 60)
        expected.drawEllipse(170, 170, 60, 60)
        expected.drawEllipse(170, 10, 60, 60)
        set_font_size(expected, 13)
        draw_text(expected, 280, 136, 'draw')
        expected.setBrush(TicTacToeDisplay.player2_colour)
        expected.drawEllipse(90, 10, 60, 60)
        expected.drawEllipse(90, 90, 60, 60)
        expected.drawEllipse(170, 90, 60, 60)
        expected.drawEllipse(10, 170, 60, 60)

        display = TicTacToeDisplay()
        display.resize(QSize(size+80, size))

        board = display.game.create_board('''\
XOX
XOO
OXX
''')
        display.update(board)

        display.scene.render(actual)


def test_coordinates(pixmap_differ: PixmapDiffer):
    with pixmap_differ.create_painters(
            250,
            200,
            'tictactoe_coordinates') as (actual, expected):
        expected.fillRect(0, 0, 250, 200, TicTacToeDisplay.background_colour)
        expected.drawLine(50, 100, 200, 100)
        expected.drawLine(50, 150, 200, 150)
        expected.drawLine(100, 50, 100, 200)
        expected.drawLine(150, 50, 150, 200)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(106, 106, 37, 37)
        set_font_size(expected, 8)
        draw_text(expected, 225, 135, 'to move')
        set_font_size(expected, 25)
        draw_text(expected, 75, 25, 'A')
        draw_text(expected, 125, 25, 'B')
        draw_text(expected, 175, 25, 'C')
        draw_text(expected, 25, 75, '1')
        draw_text(expected, 25, 125, '2')
        draw_text(expected, 25, 175, '3')
        expected.setBrush(TicTacToeDisplay.player2_colour)
        expected.drawEllipse(206, 82, 37, 37)

        display = TicTacToeDisplay()
        display.resize(QSize(250, 200))

        display.show_coordinates = True
        board = display.game.create_board('''\
  ABC
1 ...
2 .X.
3 ...
''')
        display.update(board)

        display.scene.render(actual)
