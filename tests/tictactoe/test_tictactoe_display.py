from PySide6.QtGui import QFont, QPainter, QColor, QPen
from PySide6.QtWidgets import QGraphicsScene

from zero_play.game_display import center_text_item
from zero_play.mcts_player import MctsPlayer
from zero_play.pixmap_differ import PixmapDiffer, render_display
from zero_play.tictactoe.display import TicTacToeDisplay
from zero_play.tictactoe.state import TicTacToeState


def draw_square_grid(expected):
    expected.fillRect(0, 0, 320, 240, TicTacToeDisplay.background_colour)
    expected.drawLine(0, 80, 240, 80)
    expected.drawLine(0, 160, 240, 160)
    expected.drawLine(80, 0, 80, 240)
    expected.drawLine(160, 0, 160, 240)


# noinspection DuplicatedCode
def test_start_square(pixmap_differ: PixmapDiffer):
    size = 240
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)

        display = TicTacToeDisplay()
        display.resize(324, 264)

        render_display(display, actual)
        player_pixmap = display.ui.player_pixmap.pixmap()
        assert player_pixmap.toImage() == display.player1_icon.toImage()
        assert display.ui.move_text.text() == 'to move'
        assert display.ui.black_count_pixmap.pixmap().isNull()
        assert display.ui.white_count_pixmap.pixmap().isNull()
        assert display.ui.black_count_pixmap.text() == ''
        assert display.ui.white_count_pixmap.text() == ''
        assert display.ui.black_count.text() == ''
        assert display.ui.white_count.text() == ''


def test_start_wide(pixmap_differ: PixmapDiffer):
    size = 240
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((size*2, size)) as (actual, expected):
        expected.fillRect(0, 0, size * 2 + 80, size, TicTacToeDisplay.background_colour)
        expected.drawLine(120, 80, 360, 80)
        expected.drawLine(120, 160, 360, 160)
        expected.drawLine(200, 0, 200, 240)
        expected.drawLine(280, 0, 280, 240)

        display = TicTacToeDisplay()
        display.resize(612, 264)
        render_display(display, actual)


def test_start_tall(pixmap_differ: PixmapDiffer):
    size = 120
    with pixmap_differ.create_qpainters((size, size*2)) as (actual, expected):
        expected.fillRect(0, 0, size + 40, size * 2, TicTacToeDisplay.background_colour)
        expected.drawLine(0, 100, 120, 100)
        expected.drawLine(0, 140, 120, 140)
        expected.drawLine(40, 60, 40, 180)
        expected.drawLine(80, 60, 80, 180)

        display = TicTacToeDisplay()
        display.resize(180, 264)
        render_display(display, actual)


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
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        expected.drawEllipse(90, 90, 60, 60)
        expected.setBrush(TicTacToeDisplay.player2_colour)
        expected.drawEllipse(90, 10, 60, 60)

        display = TicTacToeDisplay()
        board = TicTacToeState('''\
XO.
.X.
...
''')
        display.update_board(board)

        display.resize(324, 264)
        render_display(display, actual)

    player_pixmap = display.ui.player_pixmap.pixmap()
    assert player_pixmap.toImage() == display.player2_icon.toImage()


# noinspection DuplicatedCode
def test_piece_hover_enter(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        colour = QColor(TicTacToeDisplay.player2_colour)
        expected.setBrush(colour)
        colour.setAlpha(127)
        expected.setBrush(colour)
        colour.setRgb(0, 0, 0, 127)
        pen = QPen(colour)
        expected.setPen(pen)
        expected.drawEllipse(90, 10, 60, 60)

        display = TicTacToeDisplay()

        board = TicTacToeState('''\
X..
...
...
''')
        display.resize(324, 264)
        display.ui.game_display.grab()
        display.update_board(board)
        display.on_hover_enter(display.spaces[0][1])

        render_display(display, actual)


def test_piece_hover_enter_mcts(pixmap_differ: PixmapDiffer):
    """ Don't display move options while MCTS player is thinking. """
    size = 240
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)

        display = TicTacToeDisplay()
        player = MctsPlayer(display.start_state, TicTacToeState.X_PLAYER)
        display.mcts_players = (player, )

        display.resize(324, 264)
        display.ui.game_display.grab()
        display.on_hover_enter(display.spaces[0][1])

        render_display(display, actual)
        display.close()
    assert display.move_text.text() == 'thinking'
    expected_icon = display.player1_icon.toImage()
    assert display.ui.player_pixmap.pixmap().toImage() == expected_icon


# noinspection DuplicatedCode
def test_piece_hover_leave(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)

        display = TicTacToeDisplay()
        display.resize(324, 264)
        display.ui.game_display.grab()
        display.on_hover_enter(display.spaces[0][1])
        display.on_hover_leave(display.spaces[0][1])

        render_display(display, actual)


# noinspection DuplicatedCode
def test_piece_hover_existing(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)

        display = TicTacToeDisplay()

        board = TicTacToeState('''\
X..
...
...
''')
        display.update_board(board)
        display.resize(324, 264)
        display.ui.game_display.grab()
        display.on_hover_enter(display.spaces[0][0])

        render_display(display, actual)


def test_piece_click(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)

        display = TicTacToeDisplay()
        display.resize(324, 264)
        display.ui.game_display.grab()

        display.on_click(display.spaces[0][0])

        render_display(display, actual)


def test_winner(pixmap_differ: PixmapDiffer):
    assert 1 == 1
    size = 240
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        expected.drawEllipse(90, 90, 60, 60)
        expected.drawEllipse(170, 170, 60, 60)
        expected.setBrush(TicTacToeDisplay.player2_colour)
        expected.drawEllipse(90, 10, 60, 60)
        expected.drawEllipse(170, 90, 60, 60)

        display = TicTacToeDisplay()
        display.resize(324, 264)

        board = TicTacToeState('''\
XO.
.XO
..X
''')
        display.update_board(board)

        assert not display.spaces[0][2].isVisible()
        expected_icon = display.player1_icon.toImage()
        assert display.ui.player_pixmap.pixmap().toImage() == expected_icon
        assert display.move_text.text() == 'wins'
        render_display(display, actual)


def test_draw(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_qpainters((size, size)) as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(10, 10, 60, 60)
        expected.drawEllipse(10, 90, 60, 60)
        expected.drawEllipse(90, 170, 60, 60)
        expected.drawEllipse(170, 170, 60, 60)
        expected.drawEllipse(170, 10, 60, 60)
        expected.setBrush(TicTacToeDisplay.player2_colour)
        expected.drawEllipse(90, 10, 60, 60)
        expected.drawEllipse(90, 90, 60, 60)
        expected.drawEllipse(170, 90, 60, 60)
        expected.drawEllipse(10, 170, 60, 60)

        display = TicTacToeDisplay()
        display.resize(324, 264)

        display.update_board(display.start_state)
        board = TicTacToeState('''\
XOX
XOO
OXX
''')
        display.update_board(board)

        render_display(display, actual)
    assert display.ui.player_pixmap.pixmap().isNull()
    assert display.move_text.text() == 'draw'


def test_coordinates(pixmap_differ: PixmapDiffer):
    assert 1 == 1
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((200, 200)) as (actual, expected):
        expected.fillRect(0, 0, 250, 200, TicTacToeDisplay.background_colour)
        expected.drawLine(50, 100, 200, 100)
        expected.drawLine(50, 150, 200, 150)
        expected.drawLine(100, 50, 100, 200)
        expected.drawLine(150, 50, 150, 200)
        expected.setBrush(TicTacToeDisplay.player1_colour)
        expected.drawEllipse(106, 106, 37, 37)
        set_font_size(expected, 25)
        draw_text(expected, 75, 25, 'A')
        draw_text(expected, 125, 25, 'B')
        draw_text(expected, 175, 25, 'C')
        draw_text(expected, 25, 75, '1')
        draw_text(expected, 25, 125, '2')
        draw_text(expected, 25, 175, '3')

        display = TicTacToeDisplay()
        display.resize(276, 224)

        display.show_coordinates = True
        board = TicTacToeState('''\
  ABC
1 ...
2 .X.
3 ...
''')
        display.update_board(board)

        render_display(display, actual)
