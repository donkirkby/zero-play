from io import StringIO
from unittest.mock import patch, Mock

import numpy as np

from tests.test_mcts_player import FirstChoiceHeuristic
from zero_play.command.play import PlayController, load_arguments, get_player_summaries
from zero_play.connect4.game import Connect4Game
from zero_play.connect4.neural_net import NeuralNet
from zero_play.game import Game, GridGame
from zero_play.human_player import HumanPlayer
from zero_play.mcts_player import MctsPlayer
from zero_play.zero_play import create_parser


class FirstPlayerWinsGame(GridGame):
    name = 'First Player Wins'

    def __init__(self, board_height: int = 1, board_width: int = 1):
        super().__init__(board_height, board_width)

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

    def __init__(self, board_height: int = 1, board_width: int = 2):
        super().__init__(board_height, board_width)


class NoPlayerWinsGame(FirstPlayerWinsGame):
    name = 'No Player Wins'

    def is_win(self, board: np.ndarray, player: int):
        return False


def test_take_turn(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('2b\n'))
    parser = create_parser()
    args = parser.parse_args(['play', 'tictactoe'])
    game, players = load_arguments(args)
    controller = PlayController(game, players)
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
    game, players = load_arguments(args)
    controller = PlayController(game, players)
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
    game, players = load_arguments(args)
    controller = PlayController(game, players)
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
    game, players = load_arguments(args)
    controller = PlayController(game, players)

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


def test_display(capsys):
    game = SecondPlayerWinsGame()
    heuristic = FirstChoiceHeuristic(game)
    players = [MctsPlayer(game,
                          game.X_PLAYER,
                          iteration_count=10,
                          heuristic=heuristic),
               MctsPlayer(game,
                          game.O_PLAYER,
                          iteration_count=20,
                          heuristic=heuristic)]
    controller = PlayController(game, players)
    expected_output = """\
  AB
1 ..

  AB
1 X.

  AB
1 XO

  AB
1 ..

  AB
1 X.

  AB
1 XO

1 wins for 10 iterations
0 ties
1 wins for 20 iterations
"""

    controller.play(games=2, flip=True, display=True)

    out, err = capsys.readouterr()
    assert expected_output == out


def test_player_summaries(capsys):
    game = Connect4Game()
    players = [MctsPlayer(game,
                          game.X_PLAYER,
                          10,
                          FirstChoiceHeuristic(game)),
               HumanPlayer(game, game.O_PLAYER)]
    expected_summaries = ('mcts', 'human')

    summaries = get_player_summaries(*players)

    assert expected_summaries == summaries


def test_player_summaries_heuristic(capsys):
    game = Connect4Game()
    players = [MctsPlayer(game,
                          game.X_PLAYER,
                          10,
                          FirstChoiceHeuristic(game)),
               MctsPlayer(game,
                          game.O_PLAYER,
                          20,
                          NeuralNet(game))]
    expected_summaries = ('first choice', 'neural net')

    summaries = get_player_summaries(*players)

    assert expected_summaries == summaries


@patch('zero_play.connect4.neural_net.load_model', new=Mock())
def test_player_summaries_checkpoints(capsys, monkeypatch):
    game = Connect4Game()
    heuristic1 = NeuralNet(game)
    heuristic2 = NeuralNet(game)
    heuristic1.load_checkpoint(filename='checkpoint1.h5')
    players = [MctsPlayer(game,
                          game.X_PLAYER,
                          10,
                          heuristic1),
               MctsPlayer(game,
                          game.O_PLAYER,
                          10,
                          heuristic2)]
    expected_summaries = ('model checkpoint1.h5', 'random weights')

    summaries = get_player_summaries(*players)

    assert expected_summaries == summaries
