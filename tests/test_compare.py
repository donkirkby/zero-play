import json
from io import StringIO
from pathlib import Path

from zero_play.command.compare import choose_scenario
from zero_play.connect4.game import Connect4Game
from zero_play.connect4.neural_net import NeuralNet
from zero_play.game import Game
from zero_play.othello.game import OthelloGame
from zero_play.playout import Playout


def test_othello(tmpdir, capsys, monkeypatch):
    scenario_path = Path(tmpdir) / 'test.json'
    stdin = StringIO("""\
othello
playout
playout
Othello / Playout
""")
    monkeypatch.setattr('sys.stdin', stdin)
    expected_prompts = """\
Choose the game: [connect4], othello, tictactoe \
Choose a heuristic for player 1: [connect4], playout \
Choose a heuristic for player 2: [connect4], playout \
Enter a scenario description: \
"""
    expected_scenario_text = json.dumps(dict(command='compare',
                                             description='Othello / Playout',
                                             game='othello',
                                             heuristic=['playout', 'playout']))

    controller = choose_scenario(scenario_path)

    assert scenario_path.read_text() == expected_scenario_text
    assert capsys.readouterr().out == expected_prompts
    assert isinstance(controller.game, OthelloGame)
    player1 = controller.players[Game.X_PLAYER]
    player2 = controller.players[Game.O_PLAYER]
    assert isinstance(player1.heuristic, Playout)
    assert isinstance(player2.heuristic, Playout)


def test_connect4(tmpdir, capsys, monkeypatch):
    scenario_path = Path(tmpdir) / 'test.json'
    stdin = StringIO("""\

connect4
playout
Connect 4 / neural
""")
    monkeypatch.setattr('sys.stdin', stdin)
    expected_prompts = """\
Choose the game: [connect4], othello, tictactoe \
Choose a heuristic for player 1: [connect4], playout \
Choose a heuristic for player 2: [connect4], playout \
Enter a scenario description: \
"""
    expected_scenario_text = json.dumps(dict(command='compare',
                                             description='Connect 4 / neural',
                                             game='connect4',
                                             heuristic=['connect4', 'playout']))

    controller = choose_scenario(scenario_path)

    assert expected_scenario_text == scenario_path.read_text()
    assert expected_prompts == capsys.readouterr().out
    assert isinstance(controller.game, Connect4Game)
    player1 = controller.players[Game.X_PLAYER]
    player2 = controller.players[Game.O_PLAYER]
    assert isinstance(player1.heuristic, NeuralNet)
    assert isinstance(player2.heuristic, Playout)
