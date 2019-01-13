import numpy as np

from zero_play.playout import Playout
from zero_play.tictactoe.game import TicTacToeGame


def test_simulate_finished_game():
    game = TicTacToeGame()
    start_board = game.create_board("""\
XXX
OO.
...
""")
    expected_value = 1
    playout = Playout(game)

    value = playout.simulate(start_board)

    assert expected_value == value


def test_simulate_finished_game_for_o_player():
    game = TicTacToeGame()
    start_board = game.create_board("""\
XX.
OOO
.X.
""")
    expected_value = 1
    playout = Playout(game)

    value = playout.simulate(start_board)

    assert expected_value == value


def test_simulate_wins():
    np.random.seed(0)
    game = TicTacToeGame()
    start_board = game.create_board("""\
XOX
XO.
O..
""")
    iteration_count = 100
    expected_value_total = iteration_count / 3
    expected_low = expected_value_total * 0.9
    expected_high = expected_value_total * 1.1
    playout = Playout(game)

    value_total = 0
    for _ in range(iteration_count):
        value = playout.simulate(start_board)
        value_total += value

    assert expected_low < value_total < expected_high


def test_simulate_wins_and_losses():
    np.random.seed(0)
    game = TicTacToeGame()
    start_board = game.create_board("""\
XOX
XO.
..O
""")
    iteration_count = 200
    expected_value_total = -iteration_count / 3
    expected_low = expected_value_total * 1.1
    expected_high = expected_value_total * 0.9
    playout = Playout(game)

    value_total = 0
    for _ in range(iteration_count):
        value = playout.simulate(start_board)
        value_total += value

    assert expected_low < value_total < expected_high
