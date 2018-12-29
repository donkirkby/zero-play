from collections import Counter

from zero_play.connect4.game import Connect4Game
from zero_play.mcts_player import SearchNode, MctsPlayer
from zero_play.tictactoe.game import TicTacToeGame


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
    assert 1.0 == node.win_rate


def test_select_second_child():
    game = TicTacToeGame()
    expected_leaf_board = game.make_move(game.create_board(), 1)
    expected_leaf = SearchNode(game, expected_leaf_board)

    node = SearchNode(game)
    node.select_leaf().record_value(1)
    node.select_leaf().record_value(1)

    leaf = node.select_leaf()

    assert expected_leaf == leaf
    assert 0 == node.win_rate


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
        node.select_leaf().record_value(1)

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


def test_simulate_finished_game():
    game = TicTacToeGame()
    start_board = game.create_board("""\
XXX
OO.
...
""")
    expected_value = 1
    player = MctsPlayer(game)

    value = player.simulate(start_board)

    assert expected_value == value


def test_simulate_finished_game_for_o_player():
    game = TicTacToeGame()
    start_board = game.create_board("""\
XX.
OOO
.X.
""")
    expected_value = 1
    player = MctsPlayer(game)

    value = player.simulate(start_board)

    assert expected_value == value


def test_simulate_wins():
    game = TicTacToeGame()
    start_board = game.create_board("""\
XOX
XO.
O..
""")
    iteration_count = 1000
    expected_value_total = iteration_count / 3
    expected_low = expected_value_total * 0.9
    expected_high = expected_value_total * 1.1
    player = MctsPlayer(game)

    value_total = 0
    for _ in range(iteration_count):
        value = player.simulate(start_board)
        value_total += value

    assert expected_low < value_total < expected_high


def test_simulate_wins_and_losses():
    game = TicTacToeGame()
    start_board = game.create_board("""\
XOX
XO.
..O
""")
    iteration_count = 2000
    expected_value_total = -iteration_count / 3
    expected_low = expected_value_total * 1.1
    expected_high = expected_value_total * 0.9
    player = MctsPlayer(game)

    value_total = 0
    for _ in range(iteration_count):
        value = player.simulate(start_board)
        value_total += value

    assert expected_low < value_total < expected_high


def test_choose_move():
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
    player = MctsPlayer(game, iteration_count=2000)

    move = player.choose_move(start_board)
    board = game.make_move(start_board, move)
    display = game.display(board)

    assert expected_display == display


def test_choose_move_no_iterations():
    game = Connect4Game()
    start_board = game.create_board("""\
.......
.......
.......
...XX..
OXOXO..
XOXOXOO
""")
    test_count = 4000
    expected_count = test_count/7
    expected_low = expected_count * 0.9
    expected_high = expected_count * 1.1
    move_counts = Counter()
    for _ in range(test_count):
        player = MctsPlayer(game, iteration_count=0)

        move = player.choose_move(start_board)
        move_counts[move] += 1

    assert expected_low < move_counts[2] < expected_high
