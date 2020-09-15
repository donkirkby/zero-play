from tests.tictactoe.test_tictactoe_display import (trigger_resize, draw_text,
                                                    set_font_size)
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


# noinspection DuplicatedCode
def test_piece_count(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'othello_pieces') as (actual, expected):
        expected_display = OthelloDisplay()
        trigger_resize(expected_display, size+80, size)
        expected_scene = expected_display.scene()
        expected_scene.addRect(252, 0,
                               100, 60,
                               pen=expected_display.background_colour,
                               brush=expected_display.background_colour)
        black = expected_display.get_player_brush(1)
        white = expected_display.get_player_brush(-1)
        expected_scene.addEllipse(265, 30,
                                  10, 10,
                                  brush=black)
        expected_scene.addEllipse(285, 30,
                                  10, 10,
                                  brush=white)

        expected_scene.render(expected)
        set_font_size(expected, 10)
        draw_text(expected, 271, 50, '2')
        draw_text(expected, 291, 50, '2')

        display = OthelloDisplay()
        trigger_resize(display, size+80, size)

        display.scene().render(actual)


# noinspection DuplicatedCode
def test_piece_count_after_update(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+80,
            size,
            'othello_pieces') as (actual, expected):
        expected_display = OthelloDisplay()
        trigger_resize(expected_display, size+80, size)
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
        expected_display.update_board(state2)
        expected_scene = expected_display.scene()
        expected_scene.addRect(252, 0,
                               100, 60,
                               pen=expected_display.background_colour,
                               brush=expected_display.background_colour)
        black = expected_display.get_player_brush(1)
        white = expected_display.get_player_brush(-1)
        expected_scene.addEllipse(265, 30,
                                  10, 10,
                                  brush=black)
        expected_scene.addEllipse(285, 30,
                                  10, 10,
                                  brush=white)

        expected_scene.render(expected)
        set_font_size(expected, 10)
        draw_text(expected, 271, 50, '4')
        draw_text(expected, 291, 50, '1')

        display = OthelloDisplay()
        trigger_resize(display, size+80, size)
        display.update_board(state2)

        display.scene().render(actual)
