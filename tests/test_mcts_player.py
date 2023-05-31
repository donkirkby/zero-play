import typing
from collections import Counter

import numpy as np
from pytest import approx

from zero_play.connect4.game import Connect4State
from zero_play.game_state import GameState
from zero_play.heuristic import Heuristic
from zero_play.mcts_player import SearchNode, MctsPlayer, SearchManager
from zero_play.playout import Playout
from zero_play.tictactoe.state import TicTacToeState


class FirstChoiceHeuristic(Heuristic):
    def get_summary(self) -> typing.Sequence[str]:
        return 'first choice',

    def analyse(self, board: GameState) -> typing.Tuple[float, np.ndarray]:
        policy = self.get_policy(board)
        player = board.get_active_player()
        if board.is_win(player):
            value = 1.0
        elif board.is_win(-player):
            value = -1.0
        else:
            value = 0.0
        return value, policy

    def get_policy(self, board: GameState):
        valid_moves = board.get_valid_moves()
        if valid_moves.any():
            first_valid = np.nonzero(valid_moves)[0][0]
        else:
            first_valid = 0
        policy = np.zeros_like(valid_moves)
        policy[first_valid] = 1.0
        return policy


class EarlyChoiceHeuristic(FirstChoiceHeuristic):
    """ Thinks each move is 90% as good as the previous option. """
    def get_summary(self) -> typing.Sequence[str]:
        return 'early choice',

    def get_policy(self, board: GameState):
        valid_moves = board.get_valid_moves()
        if not valid_moves.any():
            valid_moves = (valid_moves == 0)
        raw_policy = np.multiply(valid_moves, 0.9 ** np.arange(len(valid_moves)))
        policy = raw_policy / raw_policy.sum()
        return policy


def test_repr():
    board_text = """\
.O.
.X.
...
"""
    board = TicTacToeState(board_text)
    expected_repr = "SearchNode(TicTacToeState(spaces=array([[0, -1, 0], [0, 1, 0], [0, 0, 0]])))"

    node = SearchNode(board)
    node_repr = repr(node)

    assert node_repr == expected_repr


def test_eq():
    board1 = TicTacToeState()
    board2 = TicTacToeState()
    board3 = TicTacToeState("""\
...
.X.
...
""")

    node1 = SearchNode(board1)
    node2 = SearchNode(board2)
    node3 = SearchNode(board3)

    assert node1 == node2
    assert node1 != node3
    assert node1 != 42


def test_default_board():
    expected_board = TicTacToeState()
    expected_node = SearchNode(expected_board)

    node = SearchNode(expected_board)

    assert expected_node == node


def test_select_leaf_self():
    game = TicTacToeState()
    node = SearchNode(game)
    expected_leaf = node

    leaf = node.select_leaf()

    assert expected_leaf == leaf


def test_select_first_child():
    start_state = TicTacToeState()
    expected_leaf_board = start_state.make_move(0)
    expected_leaf = SearchNode(expected_leaf_board)

    node = SearchNode(start_state)
    node.record_value(1)

    leaf = node.select_leaf()

    assert leaf == expected_leaf
    assert node.average_value == -1.0


def test_select_second_child():
    start_state = TicTacToeState()
    expected_leaf_board = start_state.make_move(1)
    expected_leaf = SearchNode(expected_leaf_board)

    node = SearchNode(start_state)
    node.select_leaf().record_value(0)
    node.select_leaf().record_value(0)

    leaf = node.select_leaf()

    assert leaf == expected_leaf
    assert node.average_value == 0


def test_select_grandchild():
    start_state = TicTacToeState()
    expected_leaf_board = TicTacToeState("""\
XO.
...
...
""")
    expected_leaf = SearchNode(expected_leaf_board)

    node = SearchNode(start_state)
    for _ in range(10):
        node.select_leaf().record_value(0)

    leaf = node.select_leaf()

    assert leaf == expected_leaf


def test_select_good_grandchild():
    start_state = TicTacToeState()
    node = SearchNode(start_state)
    node.select_leaf().record_value(0)  # Root node returns itself.
    node.select_leaf().record_value(0)  # Move 0 AT 1A, value is a tie.
    node.select_leaf().record_value(-1)  # Move 1 AT 1B, value is a win.
    # Expect it to exploit the win at 1B, and try the first grandchild at 1A.
    expected_leaf_board = TicTacToeState("""\
  ABC
1 OX.
2 ...
3 ...
""")
    expected_leaf = SearchNode(expected_leaf_board)

    leaf = node.select_leaf()

    assert leaf == expected_leaf


def test_select_no_children():
    start_board = TicTacToeState("""\
XOX
OOX
.XO
""")
    expected_leaf_board = TicTacToeState("""\
XOX
OOX
XXO
""")
    expected_leaf = SearchNode(expected_leaf_board)

    start_node = SearchNode(start_board)
    leaf1 = start_node.select_leaf()
    leaf1.record_value(1)
    leaf2 = start_node.select_leaf()
    leaf2.record_value(1)
    leaf3 = start_node.select_leaf()

    assert leaf1 == start_node
    assert leaf2 == expected_leaf
    assert leaf3 == expected_leaf


def test_choose_move():
    np.random.seed(0)
    start_state = Connect4State()
    state1 = Connect4State("""\
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
    player = MctsPlayer(start_state, iteration_count=200)

    move = player.choose_move(state1)
    state2 = state1.make_move(move)
    display = state2.display()

    assert display == expected_display


def test_choose_move_in_pool():
    start_state = Connect4State()
    state1 = Connect4State("""\
.......
.......
.......
...XX..
OXOXO..
XOXOXOO
""")
    player = MctsPlayer(start_state, milliseconds=200, process_count=2)
    valid_moves = start_state.get_valid_moves()

    move = player.choose_move(state1)

    # Can't rely on which move, because other process has separate random seed.
    assert valid_moves[move]


def test_choose_moves_at_random():
    """ Early moves are chosen from a weighted random population. """
    np.random.seed(0)
    start_state = TicTacToeState()
    state1 = TicTacToeState("""\
...
...
X..
""")
    player = MctsPlayer(start_state,
                        iteration_count=80,
                        heuristic=EarlyChoiceHeuristic())

    moves = set()
    for _ in range(10):
        move = player.choose_move(state1)
        moves.add(move)
        player.search_manager.reset()

    assert 1 < len(moves)


def test_choose_move_no_iterations():
    np.random.seed(0)
    start_state = Connect4State()
    state1 = Connect4State("""\
.......
.......
.......
...XX..
OXOXO..
XOXOXOO
""")
    test_count = 400
    expected_count = test_count/7
    expected_low = expected_count * 0.9
    expected_high = expected_count * 1.1
    move_counts = Counter()
    for _ in range(test_count):
        player = MctsPlayer(start_state, milliseconds=0)

        move = player.choose_move(state1)
        move_counts[move] += 1

    assert expected_low < move_counts[2] < expected_high


def test_analyse_finished_game():
    board = TicTacToeState("""\
OXO
XXO
XOX
""")
    heuristic = Playout()
    expected_value = 0  # A tie
    expected_policy = [1/9] * 9

    value, policy = heuristic.analyse(board)

    assert expected_value == value
    assert expected_policy == policy.tolist()


def test_search_manager_reuses_node():
    start_state = TicTacToeState()
    manager = SearchManager(start_state, Playout())
    manager.search(start_state, iterations=10)
    move = manager.get_best_move()
    state2 = start_state.make_move(move)
    node = manager.current_node

    first_value_count = node.value_count
    manager.search(state2, iterations=10)
    second_value_count = node.value_count

    assert first_value_count > 0
    assert first_value_count + 10 == second_value_count


def test_search_manager_with_opponent():
    """ Like when opponent is not sharing the SearchManager. """
    start_state = TicTacToeState()
    manager = SearchManager(start_state, Playout())
    manager.search(start_state, iterations=10)
    node = manager.current_node.children[0]  # Didn't call get_best_move().
    move = 0
    state2 = start_state.make_move(move)

    first_value_count = node.value_count
    manager.search(state2, iterations=10)
    second_value_count = node.value_count

    assert first_value_count > 0
    assert first_value_count + 10 == second_value_count


def test_annotate():
    start_state = TicTacToeState()
    player = MctsPlayer(start_state,
                        iteration_count=10,
                        heuristic=FirstChoiceHeuristic())
    player.choose_move(start_state)
    move_probabilities = player.get_move_probabilities(start_state)

    best_move, best_probability, best_count, best_value = move_probabilities[0]
    assert best_move == '1A'
    assert best_probability == approx(0.999013)
    assert best_count == 9
    assert best_value == approx(2/9)


def test_create_training_data():
    start_state = TicTacToeState()
    manager = SearchManager(start_state, FirstChoiceHeuristic())
    expected_boards, expected_outputs = zip(*[
        [start_state.get_spaces(),
         np.array([1., 0., 0., 0., 0., 0., 0., 0., 0., -1.])],
        [TicTacToeState("""\
X..
...
...
""").get_spaces(), np.array([0., 1., 0., 0., 0., 0., 0., 0., 0., 1.])],
        [TicTacToeState("""\
XO.
...
...
""").get_spaces(), np.array([0., 0., 1., 0., 0., 0., 0., 0., 0., -1.])],
        [TicTacToeState("""\
XOX
...
...
""").get_spaces(), np.array([0., 0., 0., 1., 0., 0., 0., 0., 0., 1.])],
        [TicTacToeState("""\
XOX
O..
...
""").get_spaces(), np.array([0., 0., 0., 0., 1., 0., 0., 0., 0., -1.])],
        [TicTacToeState("""\
XOX
OX.
...
""").get_spaces(), np.array([0., 0., 0., 0., 0., 1., 0., 0., 0., 1.])],
        [TicTacToeState("""\
XOX
OXO
...
""").get_spaces(), np.array([0., 0., 0., 0., 0., 0., 1., 0., 0., -1.])]])
    expected_boards = np.stack(expected_boards)
    expected_outputs = np.stack(expected_outputs)

    boards, outputs = manager.create_training_data(iterations=1, data_size=7)

    assert repr(boards) == repr(expected_boards)
    assert repr(outputs) == repr(expected_outputs)


def test_win_scores_one():
    """ Expose bug where search continues after a game-ending position. """
    state1 = TicTacToeState("""\
..X
XX.
OO.
""")

    player = MctsPlayer(TicTacToeState(), state1.X_PLAYER, milliseconds=100)

    move = player.choose_move(state1)

    search_node1 = player.search_manager.current_node.parent
    for child_node in search_node1.children:
        if child_node.move == 8:
            assert child_node.average_value == 1.0
    assert move == 8


def test_choose_move_sets_current_node():
    np.random.seed(0)
    start_state = Connect4State()
    state1 = Connect4State("""\
.......
.......
.......
.......
OXOXOXO
XOXOXOX
""")
    player = MctsPlayer(start_state, milliseconds=20)

    move1 = player.choose_move(state1)
    current_node1 = player.search_manager.current_node
    state2 = state1.make_move(move1)
    move2 = player.choose_move(state2)
    current_node2 = player.search_manager.current_node
    state3 = state2.make_move(move2)

    assert current_node1.game_state == state2
    assert current_node2.game_state == state3
