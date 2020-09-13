from tests.tictactoe.test_tictactoe_display import trigger_resize
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


def test_invalid_hover_enter(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+40,
            size,
            'othello_invalid_hover_enter') as (actual, expected):

        display = OthelloDisplay()
        trigger_resize(display, size+40, size)
        display.scene().render(expected)

        display.on_hover_enter(display.spaces[0][0])

        display.scene().render(actual)
