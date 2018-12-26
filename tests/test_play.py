from argparse import Namespace
from io import StringIO

from zero_play.command.play import PlayController
from zero_play.human_player import HumanPlayer
from zero_play.tictactoe.game import TicTacToeGame


def test_take_turn(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('2b\n'))
    player1_args = player2_args = Namespace(player=HumanPlayer)
    controller = PlayController(TicTacToeGame, player1_args, player2_args)
    expected_output = """\
  ABC
1 ...
2 ...
3 ...
Player X: 
"""

    is_finished = controller.take_turn()

    assert not is_finished
    out, err = capsys.readouterr()
    assert expected_output == out


def test(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('1C\n'))
    player1_args = player2_args = Namespace(player=HumanPlayer)
    controller = PlayController(TicTacToeGame, player1_args, player2_args)
    controller.board = controller.game.create_board("""\
  ABC
1 XX.
2 .O.
3 O..
""")
    expected_output = """\
  ABC
1 XX.
2 .O.
3 O..
Player X: 
  ABC
1 XXX
2 .O.
3 O..
Player X Wins.
"""

    is_finished = controller.take_turn()

    assert is_finished
    out, err = capsys.readouterr()
    assert expected_output == out
