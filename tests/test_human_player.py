from io import StringIO

from zero_play.human_player import HumanPlayer
from zero_play.tictactoe.game import TicTacToeGame


def test_choose_move(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('1A\n'))
    player = HumanPlayer()
    game = TicTacToeGame()
    board = game.create_board()
    moves = game.get_valid_moves(board)
    expected_move = 0
    expected_prompt = "Player X: "

    move = player.choose_move(game, board, moves)

    assert expected_move == move
    out, err = capsys.readouterr()
    assert expected_prompt == out


def test_choose_move_player_o(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('1A\n'))
    player = HumanPlayer()
    game = TicTacToeGame()
    board_text = """\
  ABC
1 .X.
2 ...
3 ...
"""
    board = game.create_board(board_text)
    moves = game.get_valid_moves(board)
    expected_move = 0
    expected_prompt = 'Player O: '

    move = player.choose_move(game, board, moves)

    assert expected_move == move
    out, err = capsys.readouterr()
    assert expected_prompt == out


def test(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('1x\n1b\n2b\n'))
    player = HumanPlayer()
    game = TicTacToeGame()
    board_text = """\
  ABC
1 .X.
2 ...
3 ...
"""
    board = game.create_board(board_text)
    moves = game.get_valid_moves(board)
    expected_move = 4
    expected_prompt = 'Player O: ' \
                      '1x is not a valid move, choose another: ' \
                      '1b is not a valid move, choose another: '

    move = player.choose_move(game, board, moves)

    assert expected_move == move
    out, err = capsys.readouterr()
    assert expected_prompt == out
