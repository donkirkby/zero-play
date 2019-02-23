from io import StringIO

import numpy as np

from zero_play.command.play import PlayController
from zero_play.game import Game
from zero_play.human_player import HumanPlayer
from zero_play.mcts_player import MctsPlayer
from zero_play.zero_play import create_parser


class FirstPlayerWinsGame(Game):
    name = 'First Player Wins'
    board_size = 1

    def create_board(self, text: str = None) -> np.ndarray:
        if text is None:
            text = '.' * self.board_size
        return np.array([self.DISPLAY_CHARS.index(c) - 1 for c in text])

    def get_spaces(self, board: np.ndarray) -> np.ndarray:
        return board

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        return board == 0

    def display(self, board: np.ndarray, show_coordinates: bool = False) -> str:
        return ''.join(self.DISPLAY_CHARS[piece + 1] for piece in board)

    def parse_move(self, text: str, board: np.ndarray) -> int:
        return int(text)

    def make_move(self, board: np.ndarray, move: int) -> np.ndarray:
        new_board = board.copy()
        new_board[move] = self.get_active_player(board)
        return new_board

    def is_win(self, board: np.ndarray, player: int) -> bool:
        if (board == 0).sum() != 0:
            return False
        x_count = (board == self.X_PLAYER).sum()
        o_count = (board == self.O_PLAYER).sum()
        if player == self.X_PLAYER:
            return o_count < x_count
        return x_count <= o_count


class SecondPlayerWinsGame(FirstPlayerWinsGame):
    name = 'Second Player Wins'
    board_size = 2


class NoPlayerWinsGame(FirstPlayerWinsGame):
    name = 'No Player Wins'

    def is_win(self, board: np.ndarray, player: int):
        return False


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


def test_play_one_first_wins():
    game = FirstPlayerWinsGame()
    controller = PlayController(game=game,
                                players=[MctsPlayer(game), MctsPlayer(game)])
    expected_p1_wins = 1
    expected_ties = 0
    expected_p2_wins = 0

    p1_wins, ties, p2_wins = controller.play()

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_play_one_second_wins():
    game = SecondPlayerWinsGame()
    controller = PlayController(game=game,
                                players=[MctsPlayer(game), MctsPlayer(game)])
    expected_p1_wins = 0
    expected_ties = 0
    expected_p2_wins = 1

    p1_wins, ties, p2_wins = controller.play()

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_play_one_tie():
    game = NoPlayerWinsGame()
    controller = PlayController(game=game,
                                players=[MctsPlayer(game), MctsPlayer(game)])
    expected_p1_wins = 0
    expected_ties = 1
    expected_p2_wins = 0

    p1_wins, ties, p2_wins = controller.play()

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_play_two():
    game = FirstPlayerWinsGame()
    controller = PlayController(game=game,
                                players=[MctsPlayer(game), MctsPlayer(game)])
    expected_p1_wins = 2
    expected_ties = 0
    expected_p2_wins = 0

    p1_wins, ties, p2_wins = controller.play(games=2)

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_play_two_flip():
    game = FirstPlayerWinsGame()
    controller = PlayController(game=game,
                                players=[MctsPlayer(game), MctsPlayer(game)])
    expected_p1_wins = 1
    expected_ties = 0
    expected_p2_wins = 1

    p1_wins, ties, p2_wins = controller.play(games=2, flip=True)

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins
