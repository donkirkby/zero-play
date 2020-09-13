import numpy as np

from zero_play.playout import Playout
from zero_play.tictactoe.state import TicTacToeState


def test_simulate_finished_game():
    start_board = TicTacToeState("""\
XXX
OO.
...
""")
    expected_value = 1
    playout = Playout()

    value = playout.simulate(start_board)

    assert value == expected_value


def test_simulate_finished_game_for_o_player():
    start_board = TicTacToeState("""\
XX.
OOO
.X.
""")
    expected_value = 1
    playout = Playout()

    value = playout.simulate(start_board)

    assert value == expected_value


def test_simulate_wins():
    np.random.seed(0)
    start_board = TicTacToeState("""\
XOX
XO.
O..
""")
    iteration_count = 100
    expected_value_total = iteration_count / 3
    expected_low = expected_value_total * 0.9
    expected_high = expected_value_total * 1.1
    playout = Playout()

    value_total = 0
    for _ in range(iteration_count):
        value = playout.simulate(start_board)
        value_total += value

    assert expected_low < value_total < expected_high


def test_simulate_wins_and_losses():
    np.random.seed(0)
    start_board = TicTacToeState("""\
XOX
XO.
..O
""")
    iteration_count = 200
    expected_value_total = -iteration_count / 3
    expected_low = expected_value_total * 1.1
    expected_high = expected_value_total * 0.9
    playout = Playout()

    value_total = 0
    for _ in range(iteration_count):
        value = playout.simulate(start_board)
        value_total += value

    assert expected_low < value_total < expected_high
