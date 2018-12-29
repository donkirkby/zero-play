import numpy as np
import pytest

from zero_play.tictactoe.game import TicTacToeGame


def test_create_board():
    expected_board = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]])
    board = TicTacToeGame().create_board()

    assert np.array_equal(expected_board, board)


def test_create_board_from_text():
    text = """\
X..
.O.
...
"""
    expected_board = np.array([[1, 0, 0],
                               [0, -1, 0],
                               [0, 0, 0]])
    board = TicTacToeGame().create_board(text)

    assert np.array_equal(expected_board, board)


def test_create_board_with_coordinates():
    text = """\
  ABC
1 X..
2 .O.
3 ...
"""
    expected_board = np.array([[1, 0, 0],
                               [0, -1, 0],
                               [0, 0, 0]])
    board = TicTacToeGame().create_board(text)

    assert np.array_equal(expected_board, board)


def test_display():
    board = np.array([[1, 0, 0],
                      [0, -1, 0],
                      [0, 0, 0]])
    expected_text = """\
X..
.O.
...
"""
    text = TicTacToeGame().display(board)

    assert expected_text == text


def test_display_coordinates():
    board = np.array([[1, 0, 0],
                      [0, -1, 0],
                      [0, 0, 0]])
    expected_text = """\
  ABC
1 X..
2 .O.
3 ...
"""
    text = TicTacToeGame().display(board, show_coordinates=True)

    assert expected_text == text


def test_get_valid_moves():
    text = """\
X..
.O.
...
"""
    expected_moves = np.array([0, 1, 1, 1, 0, 1, 1, 1, 1])
    game = TicTacToeGame()
    board = game.create_board(text)
    moves = game.get_valid_moves(board)

    assert np.array_equal(expected_moves, moves)


@pytest.mark.parametrize('move,expected_display', [
    (0, '1A'),
    (2, '1C'),
    (3, '2A'),
    (7, '3B')
])
def test_display_move(move, expected_display):
    display = TicTacToeGame().display_move(move)

    assert expected_display == display


@pytest.mark.parametrize('text,expected_move', [
    ('1A', 0),
    ('1c', 2),
    ('2A\n', 3),
    ('3B', 7)
])
def test_parse_move(text, expected_move):
    move = TicTacToeGame().parse_move(text)

    assert expected_move == move


@pytest.mark.parametrize('text,expected_message', [
    ('4B', r'Row must be between 1 and 3\.'),
    ('2D', r'Column must be between A and C\.'),
    ('2BC', r'Move must have one number and one letter\.'),
])
def test_parse_move_fails(text, expected_message):
    with pytest.raises(ValueError, match=expected_message):
        TicTacToeGame().parse_move(text)


def test_display_player_x():
    expected_display = 'Player X'

    display = TicTacToeGame().display_player(TicTacToeGame.X_PLAYER)

    assert expected_display == display


def test_display_player_o():
    expected_display = 'Player O'

    display = TicTacToeGame().display_player(TicTacToeGame.O_PLAYER)

    assert expected_display == display


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
    game = TicTacToeGame()
    board1 = game.create_board(text)
    board2 = game.make_move(board1, move)
    display = game.display(board2)

    assert expected_display == display


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
    game = TicTacToeGame()
    board1 = game.create_board(text)
    board2 = game.make_move(board1, move)
    display = game.display(board2)

    assert expected_display == display


def test_get_active_player_o():
    text = """\
XX.
.O.
...
"""
    expected_player = TicTacToeGame.O_PLAYER
    game = TicTacToeGame()
    board = game.create_board(text)
    player = game.get_active_player(board)

    assert expected_player == player


def test_get_active_player_x():
    text = """\
XX.
.OO
...
"""
    expected_player = TicTacToeGame.X_PLAYER
    game = TicTacToeGame()
    board = game.create_board(text)
    player = game.get_active_player(board)

    assert expected_player == player


def test_no_winner():
    text = """\
XX.
.OO
...
"""
    game = TicTacToeGame()
    expected_winner = game.NO_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_horizontal_winner():
    text = """\
XXX
.OO
...
"""
    game = TicTacToeGame()
    expected_winner = game.X_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_vertical_winner():
    text = """\
XXO
.OO
XXO
"""
    game = TicTacToeGame()
    expected_winner = game.O_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_diagonal_winner():
    text = """\
OX.
XOO
XXO
"""
    game = TicTacToeGame()
    expected_winner = game.O_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_not_ended():
    text = """\
OX.
XOO
XOX
"""
    expected_is_ended = False
    game = TicTacToeGame()
    board = game.create_board(text)
    is_ended = game.is_ended(board)

    assert expected_is_ended == is_ended


def test_winner_ended():
    text = """\
OX.
XOO
XXO
"""
    expected_is_ended = True
    game = TicTacToeGame()
    board = game.create_board(text)
    is_ended = game.is_ended(board)

    assert expected_is_ended == is_ended


def test_draw_ended():
    text = """\
OXX
XOO
XOX
"""
    expected_is_ended = True
    game = TicTacToeGame()
    board = game.create_board(text)
    is_ended = game.is_ended(board)

    assert expected_is_ended == is_ended
