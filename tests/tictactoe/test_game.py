import numpy as np

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


def test():
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
