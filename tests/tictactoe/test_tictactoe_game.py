from textwrap import dedent

import numpy as np
import pytest

from zero_play.tictactoe.state import TicTacToeState


def test_create_board():
    expected_spaces = np.array([[[0, 0, 0],
                                 [0, 0, 0],
                                 [0, 0, 0]],
                                [[0, 0, 0],
                                 [0, 0, 0],
                                 [0, 0, 0]]])
    board = TicTacToeState()

    assert np.array_equal(board.get_spaces(), expected_spaces)


# noinspection DuplicatedCode
def test_create_board_from_text():
    text = """\
X..
.O.
...
"""
    expected_spaces = np.array([[[1, 0, 0],
                                 [0, 0, 0],
                                 [0, 0, 0]],
                                [[0, 0, 0],
                                 [0, 1, 0],
                                 [0, 0, 0]]])
    board = TicTacToeState(text)

    assert np.array_equal(board.get_spaces(), expected_spaces)


def test_repr():
    text = dedent("""\
        X..
        .O.
        ...
        """)
    state = TicTacToeState(text)

    assert repr(state) == r"TicTacToeState('X..\n.O.\n...\n')"


# noinspection DuplicatedCode
def test_create_board_with_coordinates():
    text = """\
  ABC
1 X..
2 .O.
3 ...
"""
    expected_spaces = np.array([[[1, 0, 0],
                                 [0, 0, 0],
                                 [0, 0, 0]],
                                [[0, 0, 0],
                                 [0, 1, 0],
                                 [0, 0, 0]]])
    board = TicTacToeState(text)

    assert np.array_equal(board.get_spaces(), expected_spaces)


def test_display():
    expected_text = dedent("""\
        X..
        .O.
        ...
        """)
    board = TicTacToeState(expected_text)
    text = board.display()

    assert text == expected_text


def test_display_coordinates():
    expected_text = dedent("""\
          ABC
        1 X..
        2 .O.
        3 ...
        """)
    board = TicTacToeState(expected_text)
    text = board.display(show_coordinates=True)

    assert text == expected_text


def test_get_valid_moves():
    text = """\
X..
.O.
...
"""
    expected_moves = np.array([0, 1, 1, 1, 0, 1, 1, 1, 1])
    board = TicTacToeState(text)
    moves = board.get_valid_moves()

    assert np.array_equal(moves, expected_moves)


def test_get_valid_moves_after_win():
    """ Win gets checked in search, so don't also check in valid moves. """
    text = """\
XXX
OO.
...
"""
    expected_moves = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1])
    board = TicTacToeState(text)
    moves = board.get_valid_moves()

    assert np.array_equal(expected_moves, moves)


@pytest.mark.parametrize('text,expected_move', [
    ('1A', 0),
    ('1c', 2),
    ('2A\n', 3),
    ('3B', 7)
])
def test_parse_move(text, expected_move):
    board = TicTacToeState()
    move = board.parse_move(text)

    assert move == expected_move


@pytest.mark.parametrize('text,expected_message', [
    ('4B', r'Row must be between 1 and 3\.'),
    ('2D', r'Column must be between A and C\.'),
    ('2BC', r'A move must be a row and a column\.'),
])
def test_parse_move_fails(text, expected_message):
    board = TicTacToeState()
    with pytest.raises(ValueError, match=expected_message):
        board.parse_move(text)


def test_display_player_x():
    expected_display = 'Player X'

    display = TicTacToeState().display_player(TicTacToeState.X_PLAYER)

    assert display == expected_display


def test_display_player_o():
    expected_display = 'Player O'

    display = TicTacToeState().display_player(TicTacToeState.O_PLAYER)

    assert display == expected_display


def test_make_move():
    text = """\
X..
.O.
...
"""
    move = 3
    expected_display = """\
X..
XO.
...
"""
    board1 = TicTacToeState(text)
    board2 = board1.make_move(move)
    display = board2.display()

    assert display == expected_display


def test_make_move_o():
    text = """\
XX.
.O.
...
"""
    move = 3
    expected_display = """\
XX.
OO.
...
"""
    board1 = TicTacToeState(text)
    board2 = board1.make_move(move)
    display = board2.display()

    assert display == expected_display


def test_get_active_player_o():
    text = """\
XX.
.O.
...
"""
    expected_player = TicTacToeState.O_PLAYER
    board = TicTacToeState(text)
    player = board.get_active_player()

    assert player == expected_player


def test_get_active_player_x():
    text = """\
XX.
.OO
...
"""
    expected_player = TicTacToeState.X_PLAYER
    board = TicTacToeState(text)
    player = board.get_active_player()

    assert player == expected_player


def test_no_winner():
    text = """\
XX.
.OO
...
"""
    board = TicTacToeState(text)
    expected_winner = board.NO_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_horizontal_winner():
    text = """\
XXX
.OO
...
"""
    board = TicTacToeState(text)
    expected_winner = board.X_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_vertical_winner():
    text = """\
XXO
.OO
XXO
"""
    board = TicTacToeState(text)
    expected_winner = board.O_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_diagonal_winner():
    text = """\
OX.
XOO
XXO
"""
    board = TicTacToeState(text)
    expected_winner = board.O_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_not_ended():
    text = """\
OX.
XOO
XOX
"""
    expected_is_ended = False
    board = TicTacToeState(text)
    is_ended = board.is_ended()

    assert is_ended == expected_is_ended


def test_winner_ended():
    text = """\
OX.
XOO
XXO
"""
    expected_is_ended = True
    board = TicTacToeState(text)
    is_ended = board.is_ended()

    assert is_ended == expected_is_ended


def test_draw_ended():
    text = """\
OXX
XOO
XOX
"""
    expected_is_ended = True
    board = TicTacToeState(text)
    is_ended = board.is_ended()

    assert is_ended == expected_is_ended
