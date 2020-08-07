from PySide2.QtWidgets import QGraphicsScene

from tests.pixmap_differ import PixmapDiffer
from zero_play.othello.display import OthelloDisplay


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
    scene = QGraphicsScene(0, 0, 200, 200)
    display = OthelloDisplay(scene)
    display.on_click(display.spaces[0][0])

    state = display.game.display(display.current_board)

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
    scene = QGraphicsScene(0, 0, 200, 200)
    display = OthelloDisplay(scene)
    display.on_click(display.spaces[2][1])
    display.on_click(display.spaces[1][1])

    state = display.game.display(display.current_board)

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
    scene = QGraphicsScene(0, 0, 200, 200)
    display = OthelloDisplay(scene)
    display.update(display.game.create_board(start_state))
    display.on_click(display.spaces[0][2])

    state = display.game.display(display.current_board)

    assert state == expected_state


def test_invalid_hover_enter(pixmap_differ: PixmapDiffer):
    size = 240
    with pixmap_differ.create_painters(
            size+40,
            size,
            'othello_invalid_hover_enter') as (actual, expected):

        scene = QGraphicsScene(0, 0, size+40, size)
        display = OthelloDisplay(scene)
        scene.render(expected)

        display.on_hover_enter(display.spaces[0][0])

        scene.render(actual)
