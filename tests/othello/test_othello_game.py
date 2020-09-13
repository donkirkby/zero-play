import numpy as np
import pytest

from zero_play.connect4.neural_net import NeuralNet
from zero_play.mcts_player import SearchManager
from zero_play.othello.game import OthelloState
from zero_play.playout import Playout


def test_create_board():
    x, o = OthelloState.X_PLAYER, OthelloState.O_PLAYER
    # 6x6 grid of spaces, plus next player.
    expected_board = [0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, o, x, 0, 0,
                      0, 0, x, o, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      x]
    board = OthelloState()

    assert board.board.tolist() == expected_board


# noinspection DuplicatedCode
def test_create_board_from_text():
    x, o = OthelloState.X_PLAYER, OthelloState.O_PLAYER
    text = """\
......
......
......
......
....X.
...XO.
>O
"""
    expected_board = [0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, x, 0,
                      0, 0, 0, x, o, 0,
                      o]
    board = OthelloState(text)

    assert board.board.tolist() == expected_board


# noinspection DuplicatedCode
def test_create_board_with_coordinates():
    x, o = OthelloState.X_PLAYER, OthelloState.O_PLAYER
    text = """\
  ABCDEF
1 ......
2 ......
3 ......
4 ......
5 ....X.
6 ...XO.
>X
"""
    expected_board = [0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, x, 0,
                      0, 0, 0, x, o, 0,
                      x]
    board = OthelloState(text)

    assert board.board.tolist() == expected_board


# noinspection DuplicatedCode
def test_display():
    x, o = OthelloState.X_PLAYER, OthelloState.O_PLAYER
    board = np.array([0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, x, 0,
                      0, 0, 0, x, o, 0,
                      x])
    expected_text = """\
......
......
......
......
....X.
...XO.
>X
"""
    text = OthelloState(spaces=board).display()

    assert text == expected_text


# noinspection DuplicatedCode
def test_display_coordinates():
    x, o = OthelloState.X_PLAYER, OthelloState.O_PLAYER
    board = np.array([0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, x, 0,
                      0, 0, 0, x, o, 0,
                      x])
    expected_text = """\
  ABCDEF
1 ......
2 ......
3 ......
4 ......
5 ....X.
6 ...XO.
>X
"""
    text = OthelloState(spaces=board).display(show_coordinates=True)

    assert text == expected_text


def test_get_valid_moves():
    text = """\
  ABCDEF
1 ......
2 ......
3 ......
4 ......
5 ...OX.
6 ...XO.
>X
"""
    expected_moves = [0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 1, 0, 0,
                      0, 0, 1, 0, 0, 0,
                      0, 0, 0, 0, 0, 1,
                      0]  # Can't pass when other moves are valid.
    board = OthelloState(text)
    moves = board.get_valid_moves()

    assert moves.tolist() == expected_moves


def test_get_valid_moves_with_gap():
    text = """\
  ABCDEF
1 ......
2 ......
3 ......
4 ....X.
5 ...O..
6 ...XO.
>O
"""
    expected_moves = [[0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0]]
    board = OthelloState(text)
    moves = board.get_valid_moves()

    assert moves.astype(int)[:36].reshape((6, 6)).tolist() == expected_moves


def test_get_no_valid_moves():
    text = """\
  ABCDEF
1 ......
2 ......
3 ......
4 ......
5 ....X.
6 ...OO.
>X
"""
    expected_moves = [0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      1]  # Only move is to pass.
    board = OthelloState(text)
    moves = board.get_valid_moves()

    assert moves.tolist() == expected_moves


@pytest.mark.parametrize('text,expected_move', [
    ('1A', 0),
    ('1c\n', 2),
    (' 6 F', 35),
    ('', 36)
])
def test_parse_move(text, expected_move):
    board = OthelloState()
    move = board.parse_move(text)

    assert move == expected_move


@pytest.mark.parametrize('move,expected_text', [
    (0, '1A'),
    (64, 'PASS')
])
def test_display_move(move, expected_text):
    state = OthelloState(board_height=8, board_width=8)
    move_text = state.display_move(move)

    assert move_text == expected_text


@pytest.mark.parametrize('text,expected_message', [
    ('7C', r'Row must be between 1 and 6\.'),
    ('6G', r'Column must be between A and F\.'),
    ('2', r"A move must be a row and a column\."),
    ('23C', r"A move must be a row and a column\."),
])
def test_parse_move_fails(text, expected_message):
    state = OthelloState()
    with pytest.raises(ValueError, match=expected_message):
        state.parse_move(text)


def test_make_move():
    text = """\
......
......
......
......
......
...XO.
>X
"""
    move = 35
    expected_display = """\
......
......
......
......
......
...XXX
>O
"""
    board1 = OthelloState(text)
    board2 = board1.make_move(move)
    display = board2.display()

    assert display == expected_display


def test_make_move_pass():
    text = """\
......
......
......
......
....O.
...XX.
>O
"""
    move = 36
    expected_display = """\
......
......
......
......
....O.
...XX.
>X
"""
    board1 = OthelloState(text)
    board2 = board1.make_move(move)
    display = board2.display()

    assert display == expected_display


def test_make_move_o():
    text = """\
......
......
......
......
......
...XO.
>O
"""
    move = 32
    expected_display = """\
......
......
......
......
......
..OOO.
>X
"""
    board1 = OthelloState(text)
    board2 = board1.make_move(move)
    display = board2.display()

    assert display == expected_display


def test_get_active_player_o():
    text = """\
......
......
......
......
....X.
...XO.
>O
"""
    expected_player = OthelloState.O_PLAYER
    board = OthelloState(text)
    player = board.get_active_player()

    assert player == expected_player


def test_get_active_player_x():
    text = """\
......
......
......
......
....X.
...XO.
>X
"""
    expected_player = OthelloState.X_PLAYER
    board = OthelloState(text)
    player = board.get_active_player()

    assert player == expected_player


def test_no_winner_not_ended():
    text = """\
XXXXXX
XXXXXX
XXXXX.
OOOOOX
OOOOOO
OOOOOO
>O
"""
    board = OthelloState(text)
    expected_winner = board.NO_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner
    assert not board.is_ended()


def test_no_winner_tie():
    text = """\
XXXXXX
XXXXXX
XXXXXX
OOOOOO
OOOOOO
OOOOOO
>O
"""
    board = OthelloState(text)
    expected_winner = board.NO_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner
    assert board.is_ended()


def test_winner_x():
    text = """\
XXXXXX
XXXXXX
XXXXXX
OOOOOX
OOOOOO
OOOOOO
>O
"""
    board = OthelloState(text)
    expected_winner = board.X_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner
    assert board.is_win(expected_winner)


def test_winner_o():
    text = """\
XXXXXX
XXXXXX
XXXXXO
OOOOOO
OOOOOO
OOOOOO
>O
"""
    board = OthelloState(text)
    expected_winner = board.O_PLAYER
    winner = board.get_winner()

    assert winner == expected_winner


def test_playout():
    """ Just checking that playouts don't raise an exception. """
    board = OthelloState()
    playout = Playout()

    playout.simulate(board)


def test_pass_is_not_win():
    board = OthelloState("""\
......
......
X.....
.OO...
.OO...
......
>O
""")
    expected_valid_moves = [False] * 36 + [True]

    valid_moves = board.get_valid_moves()

    assert valid_moves.tolist() == expected_valid_moves
    assert not board.is_ended()


def test_no_moves_for_either():
    board = OthelloState("""\
......
......
......
X.....
.OO...
.OO...
>X
""")
    expected_valid_moves = [False] * 37

    valid_moves = board.get_valid_moves()

    assert valid_moves.tolist() == expected_valid_moves
    assert board.get_winner() == board.O_PLAYER


def test_create_from_array():
    board = OthelloState(spaces=np.zeros(65, dtype=np.int8))

    assert board.board_width == 8


def test_training_data():
    state = OthelloState()
    neural_net = NeuralNet(state)
    neural_net.epochs_to_train = 10
    search_manager = SearchManager(state, neural_net)
    boards, outputs = search_manager.create_training_data(
        iterations=10,
        data_size=10)
    neural_net.train(boards, outputs)
