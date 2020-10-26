import numpy as np

from tests.test_mcts_player import FirstChoiceHeuristic
from zero_play.play_controller import PlayController, PlayerResults
from zero_play.game_state import GridGameState
from zero_play.mcts_player import MctsPlayer


class FirstPlayerWinsGame(GridGameState):
    game_name = 'First Player Wins'

    def __init__(self,
                 board_height: int = 1,
                 board_width: int = 1,
                 spaces: np.ndarray = None):
        super().__init__(board_height, board_width, spaces=spaces)

    def is_win(self, player: int) -> bool:
        if (self.board == 0).sum() != 0:
            return False
        x_count = (self.board == self.X_PLAYER).sum()
        o_count = (self.board == self.O_PLAYER).sum()
        if player == self.X_PLAYER:
            return o_count < x_count
        return x_count <= o_count


class SecondPlayerWinsGame(FirstPlayerWinsGame):
    game_name = 'Second Player Wins'

    def __init__(self,
                 board_height: int = 1,
                 board_width: int = 2,
                 spaces: np.ndarray = None):
        super().__init__(board_height, board_width, spaces=spaces)


class NoPlayerWinsGame(FirstPlayerWinsGame):
    game_name = 'No Player Wins'

    def is_win(self, player: int):
        return False


def test_play_one_first_wins():
    start_state = FirstPlayerWinsGame()
    controller = PlayController(start_state=start_state,
                                players=[MctsPlayer(start_state),
                                         MctsPlayer(start_state)])
    expected_p1_wins = 1
    expected_ties = 0
    expected_p2_wins = 0

    p1_wins, ties, p2_wins = controller.play()

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_play_one_second_wins():
    start_state = SecondPlayerWinsGame()
    controller = PlayController(start_state=start_state,
                                players=[MctsPlayer(start_state),
                                         MctsPlayer(start_state)])
    expected_p1_wins = 0
    expected_ties = 0
    expected_p2_wins = 1

    p1_wins, ties, p2_wins = controller.play()

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_play_one_tie():
    start_state = NoPlayerWinsGame()
    controller = PlayController(start_state=start_state,
                                players=[MctsPlayer(start_state),
                                         MctsPlayer(start_state)])
    expected_p1_wins = 0
    expected_ties = 1
    expected_p2_wins = 0

    p1_wins, ties, p2_wins = controller.play()

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_play_two():
    start_state = FirstPlayerWinsGame()
    controller = PlayController(start_state=start_state,
                                players=[MctsPlayer(start_state),
                                         MctsPlayer(start_state)])
    expected_p1_wins = 2
    expected_ties = 0
    expected_p2_wins = 0

    p1_wins, ties, p2_wins = controller.play(games=2)

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_play_two_flip():
    start_state = FirstPlayerWinsGame()
    controller = PlayController(start_state=start_state,
                                players=[MctsPlayer(start_state),
                                         MctsPlayer(start_state)])
    expected_p1_wins = 1
    expected_ties = 0
    expected_p2_wins = 1

    p1_wins, ties, p2_wins = controller.play(games=2, flip=True)

    assert expected_p1_wins == p1_wins
    assert expected_ties == ties
    assert expected_p2_wins == p2_wins


def test_display(capsys):
    game = SecondPlayerWinsGame()
    heuristic = FirstChoiceHeuristic()
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

('mcts', 'first choice', '10 iterations') - 1 wins,
('mcts', 'first choice', '20 iterations') - 1 wins,
0 ties
"""

    controller.play(games=2, flip=True, display=True)

    out, err = capsys.readouterr()
    expected_lines = expected_output.splitlines()
    lines = out.splitlines()
    assert lines[:-3] == expected_lines[:-3]
    for line, expected_line in zip(lines[-3:], expected_lines[-3:]):
        assert line.startswith(expected_line)


def test_player_results():
    player = MctsPlayer(FirstPlayerWinsGame(), iteration_count=100)
    player_results = PlayerResults(player)
    player_results.move_count = 100
    player_results.total_time = 1246  # seconds
    player_results.win_count = 1

    summary = player_results.get_summary()

    assert summary == "('mcts', 'playout', '100 iterations') - 1 wins, 12.5s/move"
