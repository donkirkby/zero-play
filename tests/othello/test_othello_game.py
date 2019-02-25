import numpy as np
import pytest

from zero_play.connect4.neural_net import NeuralNet
from zero_play.mcts_player import SearchManager
from zero_play.othello.game import OthelloGame
from zero_play.playout import Playout


def test_create_board():
    x, o = OthelloGame.X_PLAYER, OthelloGame.O_PLAYER
    # 6x6 grid of spaces, plus next player.
    expected_board = [0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, o, x, 0, 0,
                      0, 0, x, o, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0,
                      x]
    board = OthelloGame().create_board()

    assert expected_board == board.tolist()


def test_create_board_from_text():
    x, o = OthelloGame.X_PLAYER, OthelloGame.O_PLAYER
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
    board = OthelloGame().create_board(text)

    assert expected_board == board.tolist()


def test_create_board_with_coordinates():
    x, o = OthelloGame.X_PLAYER, OthelloGame.O_PLAYER
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
    board = OthelloGame().create_board(text)

    assert expected_board == board.tolist()


def test_display():
    x, o = OthelloGame.X_PLAYER, OthelloGame.O_PLAYER
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
    text = OthelloGame().display(board)

    assert expected_text == text


def test_display_coordinates():
    x, o = OthelloGame.X_PLAYER, OthelloGame.O_PLAYER
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
    text = OthelloGame().display(board, show_coordinates=True)

    assert expected_text == text


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
    game = OthelloGame()
    board = game.create_board(text)
    moves = game.get_valid_moves(board)

    assert expected_moves == moves.tolist()


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
    game = OthelloGame()
    board = game.create_board(text)
    moves = game.get_valid_moves(board)

    assert expected_moves == moves.tolist()


@pytest.mark.parametrize('text,expected_move', [
    ('1A', 0),
    ('1c\n', 2),
    (' 6 F', 35),
    ('', 36)
])
def test_parse_move(text, expected_move):
    game = OthelloGame()
    move = game.parse_move(text, game.create_board())

    assert expected_move == move


@pytest.mark.parametrize('text,expected_message', [
    ('7C', r'Row must be between 1 and 6\.'),
    ('6G', r'Column must be between A and F\.'),
    ('2', r"A move must be a row and a column\."),
    ('23C', r"A move must be a row and a column\."),
])
def test_parse_move_fails(text, expected_message):
    game = OthelloGame()
    with pytest.raises(ValueError, match=expected_message):
        game.parse_move(text, game.create_board())


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
    game = OthelloGame()
    board1 = game.create_board(text)
    board2 = game.make_move(board1, move)
    display = game.display(board2)

    assert expected_display == display


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
    game = OthelloGame()
    board1 = game.create_board(text)
    board2 = game.make_move(board1, move)
    display = game.display(board2)

    assert expected_display == display


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
    game = OthelloGame()
    board1 = game.create_board(text)
    board2 = game.make_move(board1, move)
    display = game.display(board2)

    assert expected_display == display


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
    expected_player = OthelloGame.O_PLAYER
    game = OthelloGame()
    board = game.create_board(text)
    player = game.get_active_player(board)

    assert expected_player == player


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
    expected_player = OthelloGame.X_PLAYER
    game = OthelloGame()
    board = game.create_board(text)
    player = game.get_active_player(board)

    assert expected_player == player


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
    game = OthelloGame()
    expected_winner = game.NO_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner
    assert not game.is_ended(board)


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
    game = OthelloGame()
    expected_winner = game.NO_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner
    assert game.is_ended(board)


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
    game = OthelloGame()
    expected_winner = game.X_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner
    assert game.is_win(board, expected_winner)


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
    game = OthelloGame()
    expected_winner = game.O_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_playout():
    """ Just checking that playouts don't raise an exception. """
    game = OthelloGame()
    board = game.create_board()
    playout = Playout(game)

    playout.simulate(board)


def test_pass_is_not_win():
    game = OthelloGame()
    board = game.create_board("""\
......
......
X.....
.OO...
.OO...
......
>O
""")
    expected_valid_moves = [False] * 36 + [True]

    valid_moves = game.get_valid_moves(board)

    assert expected_valid_moves == valid_moves.tolist()
    assert not game.is_ended(board)


def test_no_moves_for_either():
    game = OthelloGame()
    board = game.create_board("""\
......
......
......
X.....
.OO...
.OO...
>X
""")
    expected_valid_moves = [False] * 37

    valid_moves = game.get_valid_moves(board)

    assert expected_valid_moves == valid_moves.tolist()
    assert game.O_PLAYER == game.get_winner(board)


def test_training_data():
    game = OthelloGame()
    neural_net = NeuralNet(game)
    neural_net.epochs_to_train = 10
    search_manager = SearchManager(game, neural_net)
    boards, outputs = search_manager.create_training_data(
        iterations=10,
        data_size=10)
    neural_net.train(boards, outputs)
