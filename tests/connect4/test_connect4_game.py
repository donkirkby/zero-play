import numpy as np
import pytest

from zero_play.connect4.game import Connect4State


def test_create_board():
    expected_spaces = np.array([[0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0]])
    board = Connect4State()

    assert np.array_equal(board.get_spaces(), expected_spaces)


# noinspection DuplicatedCode
def test_create_board_from_text():
    text = """\
.......
.......
.......
.......
....X..
...XO..
"""
    expected_spaces = np.array([[0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 1, 0, 0],
                                [0, 0, 0, 1, -1, 0, 0]])
    board = Connect4State(text)

    assert np.array_equal(board.get_spaces(), expected_spaces)


# noinspection DuplicatedCode
def test_create_board_with_coordinates():
    text = """\
1234567
.......
.......
.......
.......
....X..
...XO..
"""
    expected_board = np.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, -1, 0, 0]])
    board = Connect4State(text)

    assert np.array_equal(board.get_spaces(), expected_board)


# noinspection DuplicatedCode
def test_display():
    spaces = np.array([[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 1, -1, 0, 0]])
    expected_text = """\
.......
.......
.......
.......
....X..
...XO..
"""
    text = Connect4State(spaces=spaces).display()

    assert text == expected_text


# noinspection DuplicatedCode
def test_display_coordinates():
    spaces = np.array([[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 1, -1, 0, 0]])
    expected_text = """\
1234567
.......
.......
.......
.......
....X..
...XO..
"""
    text = Connect4State(spaces=spaces).display(show_coordinates=True)

    assert expected_text == text


def test_get_valid_moves():
    text = """\
1234567
....X..
....O..
....X..
....O..
....X..
...XO..
"""
    expected_moves = np.array([1, 1, 1, 1, 0, 1, 1])
    board = Connect4State(text)
    moves = board.get_valid_moves()

    assert np.array_equal(expected_moves, moves)


@pytest.mark.parametrize('text,expected_move', [
    ('1', 0),
    ('3\n', 2),
    (' 7', 6)
])
def test_parse_move(text, expected_move):
    game = Connect4State()
    move = game.parse_move(text)

    assert move == expected_move


@pytest.mark.parametrize('text,expected_message', [
    ('8', r'Move must be between 1 and 7\.'),
    ('2B', r"invalid literal for int\(\) with base 10: '2B'"),
])
def test_parse_move_fails(text, expected_message):
    game = Connect4State()
    with pytest.raises(ValueError, match=expected_message):
        game.parse_move(text)


def test_display_player_x():
    expected_display = 'Player X'

    display = Connect4State().display_player(Connect4State.X_PLAYER)

    assert display == expected_display


def test_display_player_o():
    expected_display = 'Player O'

    display = Connect4State().display_player(Connect4State.O_PLAYER)

    assert display == expected_display


def test_make_move():
    text = """\
.......
.......
.......
.......
.......
...XO..
"""
    move = 4
    expected_display = """\
.......
.......
.......
.......
....X..
...XO..
"""
    board1 = Connect4State(text)
    board2 = board1.make_move(move)
    display = board2.display()

    assert display == expected_display


def test_make_move_o():
    text = """\
.......
.......
.......
.......
....X..
...XO..
"""
    move = 4
    expected_display = """\
.......
.......
.......
....O..
....X..
...XO..
"""
    board1 = Connect4State(text)
    board2 = board1.make_move(move)
    display = board2.display()

    assert display == expected_display


def test_get_active_player_o():
    text = """\
.......
.......
.......
.......
....X..
...XO..
"""
    expected_player = Connect4State.O_PLAYER
    board = Connect4State(text)
    player = board.get_active_player()

    assert player == expected_player


def test_get_active_player_x():
    text = """\
.......
.......
.......
....O..
....X..
...XO..
"""
    expected_player = Connect4State.X_PLAYER
    board = Connect4State(text)
    player = board.get_active_player()

    assert player == expected_player


def test_no_winner():
    text = """\
.......
.......
.......
.......
...OO..
X.XXXO.
"""
    board = Connect4State(text)
    expected_winner = board.NO_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_horizontal_winner():
    text = """\
.......
.......
.......
.......
...OO..
.XXXXO.
"""
    board = Connect4State(text)
    expected_winner = board.X_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_horizontal_end_winner():
    text = """\
.......
.......
.......
.......
...OO..
..OXXXX
"""
    board = Connect4State(text)
    expected_winner = board.X_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_longer_winner():
    text = """\
.......
.......
.......
.......
..OOO..
XXXXXO.
"""
    board = Connect4State(text)
    expected_winner = board.X_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_vertical_winner():
    text = """\
.......
.....O.
.....O.
....XO.
..XXXO.
"""
    board = Connect4State(text)
    expected_winner = board.O_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_diagonal1_winner():
    text = """\
.......
..O....
..XO...
..OXO..
..XXXO.
"""
    board = Connect4State(text)
    expected_winner = board.O_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_diagonal2_winner():
    text = """\
......X
.....XO
..XOXOX
..OXOXO
..OXXXO
"""
    board = Connect4State(text)
    expected_winner = board.X_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_diagonal2_bottom_winner():
    text = """\
.......
.......
....X..
...XO..
..XOO..
.XOXOX.
"""
    board = Connect4State(text)
    expected_winner = board.X_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_diagonal2_left_winner():
    text = """\
.......
.......
...O...
..OX...
.OXX...
OXXO...
"""
    board = Connect4State(text)
    expected_winner = board.O_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner
