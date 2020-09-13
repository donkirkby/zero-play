import json
from pathlib import Path

import numpy as np

from zero_play.connect4.game import Connect4State
from zero_play.connect4.neural_net import NeuralNet


def test_end_game_value():
    board = Connect4State("""\
.......
.......
.......
.......
OOO....
XXXX...
""")
    heuristic = NeuralNet(board)
    expected_value = 1.0
    expected_policy = [1/7] * 7

    value, policy = heuristic.analyse(board)

    assert expected_value == value
    assert expected_policy == policy.tolist()


def test_train():
    training_path = Path(__file__).parent / 'training_data.json'
    boards_list, outputs_list = json.loads(training_path.read_text())
    boards = np.array(boards_list)
    outputs = np.array(outputs_list)

    board = Connect4State()
    neural_net = NeuralNet(board)

    history = neural_net.train(boards, outputs)

    assert history is not None
