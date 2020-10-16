from PySide2.QtCore import QSize
from PySide2.QtGui import QFont, QPainter, QColor, QPen
from PySide2.QtWidgets import QGraphicsScene, QGraphicsView

from zero_play.game_display import center_text_item, GameDisplay
from zero_play.mcts_player import MctsPlayer
from zero_play.pixmap_differ import PixmapDiffer
from zero_play.tictactoe.display import TicTacToeDisplay
from zero_play.tictactoe.state import TicTacToeState


def draw_square_grid(expected):
    expected.fillRect(0, 0, 320, 240, TicTacToeDisplay.background_colour)
    expected.drawLine(0, 80, 240, 80)
    expected.drawLine(0, 160, 240, 160)
    expected.drawLine(80, 0, 80, 240)
    expected.drawLine(160, 0, 160, 240)


def render_display(display: GameDisplay,
                   painter: QPainter,
                   is_closed: bool = True):
    """ Check scene size, render, then clear scene.

    You have to clear the scene to avoid a crash after running several unit
    tests.
    :param display: display widget whose children contain a QGraphicsView to
        render.
    :param painter: a canvas to render on
    :param is_closed: True if the display should be closed after rendering. Be
        sure to close the display before exiting the test, if it contains any
        items with reference cycles back to the scene.
    """
    __tracebackhide__ = True
    try:
        for child in display.children():
            if isinstance(child, QGraphicsView):
                view = child
                break
        else:
            raise ValueError("No QGraphicsView in display's children.")

        view.grab()  # Force layout to recalculate, if needed.
        scene_size = view.contentsRect().size()
        painter_size = painter.device().size()
        if scene_size != painter_size:
            display_size = find_display_size(display, view, painter_size)
            message = (f"Try resizing display to "
                       f"{display_size.width()}x{display_size.height()}.")
            painter.drawText(0, painter_size.height()//2, message)
            return
        assert scene_size == painter_size
        view.scene().render(painter)
    finally:
        if is_closed:
            display.close()


def find_display_size(display: GameDisplay,
                      view: QGraphicsView,
                      target_size: QSize) -> QSize:
    max_width = None
    max_height = None
    min_width = min_height = 1
    display_width = display.width()
    display_height = display.height()
    while True:
        scene_size = view.contentsRect().size()
        if scene_size.width() == target_size.width():
            min_width = max_width = display_width
        elif scene_size.width() < target_size.width():
            min_width = display_width+1
        else:
            max_width = display_width-1
        if scene_size.height() == target_size.height():
            min_height = max_height = display_height
        elif scene_size.height() < target_size.height():
            min_height = display_height+1
        else:
            max_height = display_height-1
        if max_width is None:
            display_width *= 2
        else:
            display_width = (min_width + max_width) // 2
        if max_height is None:
            display_height *= 2
        else:
            display_height = (min_height + max_height) // 2
        if min_width == max_width and min_height == max_height:
            return QSize(display_width, display_height)
        display.resize(display_width, display_height)
        view.grab()  # Force layout recalculation.


# noinspection DuplicatedCode
def test_start_square(pixmap_differ: PixmapDiffer):
    size = 240
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_start_square') as (actual, expected):
        draw_square_grid(expected)
        expected.setBrush(TicTacToeDisplay.player1_colour)

        display = TicTacToeDisplay()
        display.resize(324, 264)

        render_display(display, actual)
        player_pixmap = display.ui.player_pixmap.pixmap()
        assert player_pixmap.toImage() == display.player1_icon.toImage()
        assert display.ui.move_text.text() == 'to move'
        assert display.ui.black_count_pixmap.pixmap() is None
        assert display.ui.white_count_pixmap.pixmap() is None
        assert display.ui.black_count_pixmap.text() == ''
        assert display.ui.white_count_pixmap.text() == ''
        assert display.ui.black_count.text() == ''
        assert display.ui.white_count.text() == ''


def test_start_wide(pixmap_differ: PixmapDiffer):
    size = 240
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(
            size*2,
            size,
            'tictactoe_start_wide') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size*2,
            'tictactoe_start_tall') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_pieces') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_piece_hover_enter') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_piece_hover_enter_mcts') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_piece_hover_leave') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_piece_hover_existing') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_piece_click') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_winner') as (actual, expected):
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
    with pixmap_differ.create_painters(
            size,
            size,
            'tictactoe_draw') as (actual, expected):
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
    assert display.ui.player_pixmap.pixmap() is None
    assert display.move_text.text() == 'draw'


def test_coordinates(pixmap_differ: PixmapDiffer):
    assert 1 == 1
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(
            200,
            200,
            'tictactoe_coordinates') as (actual, expected):
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
