from io import StringIO

from zero_play.command.play import PlayController
from zero_play.game import Game
from zero_play.human_player import HumanPlayer
from zero_play.mcts_player import MctsPlayer
from zero_play.zero_play import create_parser


def test_take_turn(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('2b\n'))
    parser = create_parser()
    args = parser.parse_args(['play', 'tictactoe'])
    controller = PlayController(args)
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


def test_winning_turn(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('1C\n'))
    parser = create_parser()
    args = parser.parse_args(['play', 'tictactoe'])
    controller = PlayController(args)
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


def test_draw(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('2A\n'))
    parser = create_parser()
    args = parser.parse_args(['play', 'tictactoe'])
    controller = PlayController(args)
    controller.board = controller.game.create_board("""\
  ABC
1 XOX
2 .OX
3 OXO
""")
    expected_output = """\
  ABC
1 XOX
2 .OX
3 OXO
Player X: 
  ABC
1 XOX
2 XOX
3 OXO
The game is a draw.
"""

    is_finished = controller.take_turn()

    assert is_finished
    out, err = capsys.readouterr()
    assert expected_output == out


def test_different_players(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('2A\n'))
    parser = create_parser()
    args = parser.parse_args(['play', 'tictactoe', '--players', 'human', 'mcts'])
    controller = PlayController(args)

    assert isinstance(controller.players[Game.X_PLAYER], HumanPlayer)
    assert isinstance(controller.players[Game.O_PLAYER], MctsPlayer)
