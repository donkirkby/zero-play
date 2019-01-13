import typing
from collections import Counter

import numpy as np

from zero_play.connect4.game import Connect4Game
from zero_play.heuristic import Heuristic
from zero_play.mcts_player import SearchNode, MctsPlayer, SearchManager
from zero_play.playout import Playout
from zero_play.tictactoe.game import TicTacToeGame


class FirstChoiceHeuristic(Heuristic):
    def analyse(self, board: np.ndarray) -> typing.Tuple[float, np.ndarray]:
        valid_moves = self.game.get_valid_moves(board)
        if self.game.is_ended(board):
            opponent = -self.game.get_active_player(board)
            value = -1.0 if self.game.is_win(board, opponent) else 1.0
            policy = np.ones_like(valid_moves) / len(valid_moves)
        else:
            value = 1.0
            first_valid = np.nonzero(valid_moves)[0][0]
            policy = np.zeros_like(valid_moves)
            policy[first_valid] = 1.0
        return value, policy


def test_repr():
    game = TicTacToeGame()
    board_text = """\
.O.
.X.
...
"""
    board = game.create_board(board_text)
    expected_repr = "SearchNode(TicTacToeGame(), array([[0, -1, 0], [0, 1, 0], [0, 0, 0]]))"

    node = SearchNode(game, board)
    node_repr = repr(node)

    assert expected_repr == node_repr


def test_eq():
    game = TicTacToeGame()
    board1 = game.create_board()
    board2 = game.create_board()
    board3 = game.create_board("""\
...
.X.
...
""")

    node1 = SearchNode(game, board1)
    node2 = SearchNode(game, board2)
    node3 = SearchNode(game, board3)

    assert node1 == node2
    assert node1 != node3
    assert node1 != 42


def test_default_board():
    game = TicTacToeGame()
    expected_board = game.create_board()
    expected_node = SearchNode(game, expected_board)

    node = SearchNode(game)

    assert expected_node == node


def test_select_leaf_self():
    game = TicTacToeGame()
    node = SearchNode(game)
    expected_leaf = node

    leaf = node.select_leaf()

    assert expected_leaf == leaf


def test_select_first_child():
    game = TicTacToeGame()
    expected_leaf_board = game.make_move(game.create_board(), 0)
    expected_leaf = SearchNode(game, expected_leaf_board)

    node = SearchNode(game)
    node.record_value(1)

    leaf = node.select_leaf()

    assert expected_leaf == leaf
    assert 1.0 == node.average_value


def test_select_second_child():
    game = TicTacToeGame()
    expected_leaf_board = game.make_move(game.create_board(), 1)
    expected_leaf = SearchNode(game, expected_leaf_board)

    node = SearchNode(game)
    node.select_leaf().record_value(0)
    node.select_leaf().record_value(0)

    leaf = node.select_leaf()

    assert expected_leaf == leaf
    assert 0 == node.average_value


def test_select_grandchild():
    game = TicTacToeGame()
    expected_leaf_board = game.create_board("""\
XO.
...
...
""")
    expected_leaf = SearchNode(game, expected_leaf_board)

    node = SearchNode(game)
    for _ in range(10):
        node.select_leaf().record_value(0)

    leaf = node.select_leaf()

    assert expected_leaf == leaf


def test_select_good_grandchild():
    game = TicTacToeGame()
    node = SearchNode(game)
    node.select_leaf().record_value(0)  # Root node returns itself.
    node.select_leaf().record_value(0)  # Move 0 AT 1A, value is a tie.
    node.select_leaf().record_value(1)  # Move 1 AT 1B, value is a win.
    # Expect it to exploit the win at 1B, and try the first grandchild at 1A.
    expected_leaf_board = game.create_board("""\
  ABC
1 OX.
2 ...
3 ...
""")
    expected_leaf = SearchNode(game, expected_leaf_board)

    leaf = node.select_leaf()

    assert expected_leaf == leaf


def test_select_no_children():
    game = TicTacToeGame()
    start_board = game.create_board("""\
XOX
OOX
.XO
""")
    expected_leaf_board = game.create_board("""\
XOX
OOX
XXO
""")
    expected_leaf = SearchNode(game, expected_leaf_board)

    start_node = SearchNode(game, start_board)
    leaf1 = start_node.select_leaf()
    leaf1.record_value(1)
    leaf2 = start_node.select_leaf()
    leaf2.record_value(1)
    leaf3 = start_node.select_leaf()

    assert start_node == leaf1
    assert expected_leaf == leaf2
    assert expected_leaf == leaf3


def test_choose_move():
    np.random.seed(0)
    game = Connect4Game()
    start_board = game.create_board("""\
.......
.......
.......
...XX..
OXOXO..
XOXOXOO
""")
    expected_display = """\
.......
.......
.......
..XXX..
OXOXO..
XOXOXOO
"""
    player = MctsPlayer(game, mcts_iterations=[200])

    move = player.choose_move(start_board)
    board = game.make_move(start_board, move)
    display = game.display(board)

    assert expected_display == display


def test_choose_move_no_iterations():
    np.random.seed(0)
    game = Connect4Game()
    start_board = game.create_board("""\
.......
.......
.......
...XX..
OXOXO..
XOXOXOO
""")
    test_count = 200
    expected_count = test_count/7
    expected_low = expected_count * 0.9
    expected_high = expected_count * 1.1
    move_counts = Counter()
    for _ in range(test_count):
        player = MctsPlayer(game, mcts_iterations=[0])

        move = player.choose_move(start_board)
        move_counts[move] += 1

    assert expected_low < move_counts[2] < expected_high


def test_analyse_finished_game():
    game = TicTacToeGame()
    board = game.create_board("""\
OXO
XXO
XOX
""")
    heuristic = Playout(game)
    expected_value = 0  # A tie
    expected_policy = [1/9] * 9

    value, policy = heuristic.analyse(board)

    assert expected_value == value
    assert expected_policy == policy.tolist()


def test_search_manager_reuses_node():
    game = TicTacToeGame()
    manager = SearchManager(game, Playout(game))
    board1 = game.create_board()
    manager.search(board1, iterations=10)
    move = manager.get_best_move()
    board2 = game.make_move(board1, move)
    node = manager.current_node

    first_value_count = node.value_count
    manager.search(board2, iterations=10)
    second_value_count = node.value_count

    assert first_value_count > 0
    assert first_value_count + 10 == second_value_count


def test_search_manager_with_opponent():
    """ Like when opponent is not sharing the SearchManager. """
    game = TicTacToeGame()
    manager = SearchManager(game, Playout(game))
    board1 = game.create_board()
    manager.search(board1, iterations=10)
    node = manager.current_node.children[0]  # Didn't call get_best_move().
    move = 0
    board2 = game.make_move(board1, move)

    first_value_count = node.value_count
    manager.search(board2, iterations=10)
    second_value_count = node.value_count

    assert first_value_count > 0
    assert first_value_count + 10 == second_value_count


def test_create_training_data():
    game = TicTacToeGame()
    manager = SearchManager(game, FirstChoiceHeuristic(game))
    expected_data = [
        [game.create_board(), np.array([1., 0., 0., 0., 0., 0., 0., 0., 0.]), -1.],
        [game.create_board("""\
X..
...
...
"""), np.array([0., 1., 0., 0., 0., 0., 0., 0., 0.]), 1.],
        [game.create_board("""\
XO.
...
...
"""), np.array([0., 0., 1., 0., 0., 0., 0., 0., 0.]), -1.],
        [game.create_board("""\
XOX
...
...
"""), np.array([0., 0., 0., 1., 0., 0., 0., 0., 0.]), 1.],
        [game.create_board("""\
XOX
O..
...
"""), np.array([0., 0., 0., 0., 1., 0., 0., 0., 0.]), -1.],
        [game.create_board("""\
XOX
OX.
...
"""), np.array([0., 0., 0., 0., 0., 1., 0., 0., 0.]), 1.],
        [game.create_board("""\
XOX
OXO
...
"""), np.array([0., 0., 0., 0., 0., 0., 1., 0., 0.]), -1.]]

    training_data = manager.create_training_data(iterations=1, min_size=1)

    assert repr(expected_data) == repr(training_data)
