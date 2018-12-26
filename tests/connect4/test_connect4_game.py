import numpy as np
import pytest

from zero_play.connect4.game import Connect4Game


def test_create_board():
    expected_board = np.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]])
    board = Connect4Game().create_board()

    assert np.array_equal(expected_board, board)


def test_create_board_from_text():
    text = """\
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
    board = Connect4Game().create_board(text)

    assert np.array_equal(expected_board, board)


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
    board = Connect4Game().create_board(text)

    assert np.array_equal(expected_board, board)


def test_display():
    board = np.array([[0, 0, 0, 0, 0, 0, 0],
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
    text = Connect4Game().display(board)

    assert expected_text == text


def test_display_coordinates():
    board = np.array([[0, 0, 0, 0, 0, 0, 0],
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
    text = Connect4Game().display(board, show_coordinates=True)

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
    game = Connect4Game()
    board = game.create_board(text)
    moves = game.get_valid_moves(board)

    assert np.array_equal(expected_moves, moves)


@pytest.mark.parametrize('move,expected_display', [
    (0, '1'),
    (2, '3'),
    (6, '7')
])
def test_display_move(move, expected_display):
    display = Connect4Game().display_move(move)

    assert expected_display == display


@pytest.mark.parametrize('text,expected_move', [
    ('1', 0),
    ('3\n', 2),
    (' 7', 6)
])
def test_parse_move(text, expected_move):
    move = Connect4Game().parse_move(text)

    assert expected_move == move


@pytest.mark.parametrize('text,expected_message', [
    ('8', r'Move must be between 1 and 7\.'),
    ('2B', r"invalid literal for int\(\) with base 10: '2B'"),
])
def test_parse_move_fails(text, expected_message):
    with pytest.raises(ValueError, match=expected_message):
        Connect4Game().parse_move(text)


def test_display_player_x():
    expected_display = 'Player X'

    display = Connect4Game().display_player(Connect4Game.X_PLAYER)

    assert expected_display == display


def test_display_player_o():
    expected_display = 'Player O'

    display = Connect4Game().display_player(Connect4Game.O_PLAYER)

    assert expected_display == display


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
    game = Connect4Game()
    board1 = game.create_board(text)
    board2 = game.make_move(board1, move)
    display = game.display(board2)

    assert expected_display == display


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
    game = Connect4Game()
    board1 = game.create_board(text)
    board2 = game.make_move(board1, move)
    display = game.display(board2)

    assert expected_display == display


def test_get_active_player_o():
    text = """\
.......
.......
.......
.......
....X..
...XO..
"""
    expected_player = Connect4Game.O_PLAYER
    game = Connect4Game()
    board = game.create_board(text)
    player = game.get_active_player(board)

    assert expected_player == player


def test_get_active_player_x():
    text = """\
.......
.......
.......
....O..
....X..
...XO..
"""
    expected_player = Connect4Game.X_PLAYER
    game = Connect4Game()
    board = game.create_board(text)
    player = game.get_active_player(board)

    assert expected_player == player


def test_no_winner():
    text = """\
.......
.......
.......
.......
....O..
..XXXO.
"""
    game = Connect4Game()
    expected_winner = game.NO_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_horizontal_winner():
    text = """\
.......
.......
.......
.......
...OO..
.XXXXO.
"""
    game = Connect4Game()
    expected_winner = game.X_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_longer_winner():
    text = """\
.......
.......
.......
.......
..OOO..
XXXXXO.
"""
    game = Connect4Game()
    expected_winner = game.X_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_vertical_winner():
    text = """\
.......
.....O.
.....O.
....XO.
..XXXO.
"""
    game = Connect4Game()
    expected_winner = game.O_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_diagonal1_winner():
    text = """\
.......
..O....
..XO...
..OXO..
..XXXO.
"""
    game = Connect4Game()
    expected_winner = game.O_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner


def test_diagonal2_winner():
    text = """\
......X
.....XO
..XOXOX
..OXOXO
..OXXXO
"""
    game = Connect4Game()
    expected_winner = game.X_PLAYER
    board = game.create_board(text)
    winner = game.get_winner(board)

    assert expected_winner == winner
