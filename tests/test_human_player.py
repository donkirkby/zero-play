from io import StringIO

from zero_play.human_player import HumanPlayer
from zero_play.tictactoe.game import TicTacToeGame


def test_choose_move(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('1A\n'))
    game = TicTacToeGame()
    player = HumanPlayer(game)
    board = game.create_board()
    expected_move = 0
    expected_prompt = "Player X: "

    move = player.choose_move(board)

    assert expected_move == move
    out, err = capsys.readouterr()
    assert expected_prompt == out


def test_choose_move_player_o(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('1A\n'))
    game = TicTacToeGame()
    player = HumanPlayer(game)
    board_text = """\
  ABC
1 .X.
2 ...
3 ...
"""
    board = game.create_board(board_text)
    expected_move = 0
    expected_prompt = 'Player O: '

    move = player.choose_move(board)

    assert expected_move == move
    out, err = capsys.readouterr()
    assert expected_prompt == out


def test_invalid_moves(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('1x\n1b\n2b\n'))
    game = TicTacToeGame()
    player = HumanPlayer(game)
    board_text = """\
  ABC
1 .X.
2 ...
3 ...
"""
    board = game.create_board(board_text)
    expected_move = 4
    expected_prompt = 'Player O: ' \
                      '1x is not a valid move, choose another: ' \
                      '1b is not a valid move, choose another: '

    move = player.choose_move(board)

    assert expected_move == move
    out, err = capsys.readouterr()
    assert expected_prompt == out
