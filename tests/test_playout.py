import numpy as np

from zero_play.game_state import GameState
from zero_play.playout import Playout
from zero_play.tictactoe.state import TicTacToeState


class TakeOneTwiceGame(GameState):
    """ Silly game for testing multiple moves in a turn.

    The game starts with a numerical value, and each player makes two moves in
    each turn, where a move is subtracting one or two from the value. Win if you
    bring the value to zero.
    """
    game_name = 'Take One Twice'

    def __init__(self, value: int, move_count: int = 0):
        super().__init__()
        self.value = value
        self.move_count = move_count

    def __repr__(self):
        return f'TakeOneTwiceGame({self.value}, {self.move_count})'

    def __eq__(self, other) -> bool:
        if not isinstance(other, TakeOneTwiceGame):
            return False
        return (self.value, self.move_count % 4) == (other.value,
                                                     other.move_count % 4)

    def get_valid_moves(self) -> np.ndarray:
        """ Possible moves are subtracting 1 and subtracting 2. """
        return np.array([self.value >= 1, self.value >= 2], dtype=bool)

    def display(self, show_coordinates: bool = False) -> str:
        return f'{self.move_count}: {self.value}'

    def display_move(self, move: int) -> str:
        return str(move+1)

    def get_move_count(self) -> int:
        return self.move_count

    def spaces(self) -> np.ndarray:
        return np.ndarray([self.value, self.move_count+1])

    def parse_move(self, text: str) -> int:
        return int(text) - 1

    def make_move(self, move: int) -> 'GameState':
        return TakeOneTwiceGame(self.value-move-1, self.move_count+1)

    def calculate_player(self, move_count: int) -> int:
        if move_count % 4 < 2:
            return self.X_PLAYER
        return self.O_PLAYER

    def is_win(self, player: int) -> bool:
        if self.value > 0:
            return False
        previous_move = self.move_count - 1
        previous_player = self.calculate_player(previous_move)
        return player == previous_player

    def get_active_player(self) -> int:
        return self.calculate_player(self.move_count)


def test_simulate_finished_game():
    start_board = TicTacToeState("""\
XXX
OO.
...
""")
    expected_value = -1
    playout = Playout()

    value = playout.simulate(start_board)

    assert value == expected_value


def test_simulate_finished_game_for_o_player():
    start_board = TicTacToeState("""\
XX.
OOO
.X.
""")
    expected_value = -1
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
    expected_value_total = -iteration_count / 3
    expected_low = expected_value_total * 1.1
    expected_high = expected_value_total * 0.9
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
    expected_value_total = iteration_count / 3
    expected_low = expected_value_total * 0.9
    expected_high = expected_value_total * 1.1
    playout = Playout()

    value_total = 0
    for _ in range(iteration_count):
        value = playout.simulate(start_board)
        value_total += value

    assert expected_low < value_total < expected_high


def test_two_moves_per_turn():
    start_board = TakeOneTwiceGame(2)
    playout = Playout()

    iteration_count = 10
    expected_value_total = 10
    value_total = 0
    for _ in range(iteration_count):
        value = playout.simulate(start_board)
        value_total += value

    assert value_total == expected_value_total


def test_long_simulation():
    start_state = TakeOneTwiceGame(1500)
    playout = Playout()

    value = playout.simulate(start_state)

    assert value == 1
