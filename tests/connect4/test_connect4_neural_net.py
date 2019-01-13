import json
from pathlib import Path

from zero_play.connect4.game import Connect4Game
from zero_play.connect4.neural_net import NeuralNet


def test_end_game_value():
    game = Connect4Game()
    heuristic = NeuralNet(game)
    board = game.create_board("""\
.......
.......
.......
.......
OOO....
XXXX...
""")
    expected_value = 1.0
    expected_policy = [1/7] * 7

    value, policy = heuristic.analyse(board)

    assert expected_value == value
    assert expected_policy == policy.tolist()


def test_train():
    training_path = Path(__file__).parent / 'training_data.json'
    training_data = json.loads(training_path.read_text())

    game = Connect4Game()
    neural_net = NeuralNet(game)

    neural_net.train(training_data)
