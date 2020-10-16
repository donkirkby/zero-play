from tests.tictactoe.test_tictactoe_display import render_display
from zero_play.othello.display import OthelloDisplay
from zero_play.othello.game import OthelloState
from zero_play.pixmap_differ import PixmapDiffer


def test_piece_click_invalid(pixmap_differ: PixmapDiffer):
    expected_state = """\
......
......
..OX..
..XO..
......
......
>X
"""
    display = OthelloDisplay(6, 6)

    display.on_click(display.spaces[0][0])

    state = display.current_state.display()

    assert state == expected_state
    display.close()


def test_piece_click_valid():
    expected_state = """\
......
.O....
.XOX..
..XO..
......
......
>X
"""
    display = OthelloDisplay(6, 6)
    display.on_click(display.spaces[2][1])
    display.on_click(display.spaces[1][1])

    state = display.current_state.display()

    assert state == expected_state
    display.close()


def test_piece_click_then_pass(pixmap_differ: PixmapDiffer):
    start_state = """\
OX....
.X....
......
......
......
......
>O
"""
    expected_state = """\
OOO...
.X....
......
......
......
......
>O
"""
    display = OthelloDisplay(6, 6)
    display.update_board(OthelloState(start_state))
    display.on_click(display.spaces[0][2])

    state = display.current_state.display()

    assert state == expected_state
    display.close()


def test_invalid_hover_enter(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size,
            size,
            'othello_invalid_hover_enter') as (actual, expected):

        display = OthelloDisplay()
        display.resize(324, 264)
        render_display(display, expected, is_closed=False)

        display.on_hover_enter(display.spaces[0][0])

        render_display(display, actual)


# noinspection DuplicatedCode
def test_piece_count(pixmap_differ: PixmapDiffer):
    display = OthelloDisplay()
    assert display.ui.black_count.text() == '2'
    assert display.ui.white_count.text() == '2'
    black_count_icon = display.ui.black_count_pixmap.pixmap()
    assert black_count_icon.toImage() == display.player1_icon.toImage()
    white_count_icon = display.ui.white_count_pixmap.pixmap()
    assert white_count_icon.toImage() == display.player2_icon.toImage()
    display.close()


# noinspection DuplicatedCode
def test_piece_count_after_update(pixmap_differ: PixmapDiffer):
    display = OthelloDisplay()
    state2 = OthelloState(board_width=8, board_height=8, text="""\
........
........
........
...OX...
...XXX..
........
........
........
>O
""")
    display.update_board(state2)
    assert display.ui.black_count.text() == '4'
    assert display.ui.white_count.text() == '1'
    display.close()
