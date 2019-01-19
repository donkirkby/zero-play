import pytest

from zero_play.command.plot_strengths import MatchUp, WinCounter


def test_key():
    match_up = MatchUp(p1_iterations=8, p2_iterations=64)
    expected_key = (8, 64)

    key = match_up.key
    assert expected_key == key


@pytest.mark.parametrize(
    "result,expected_p1_wins,expected_ties,expected_p2_wins",
    [(1, 1, 0, 0),
     (0.001, 1, 0, 0),
     (0, 0, 1, 0),
     (-0.001, 0, 0, 1),
     (-1, 0, 0, 1)])
def test_record_result(result, expected_p1_wins, expected_ties, expected_p2_wins):
    match_up = MatchUp(8, 64)

    match_up.record_result(result)

    assert expected_p1_wins == match_up.p1_wins
    assert expected_ties == match_up.ties
    assert expected_p2_wins == match_up.p2_wins


def test_matchup_repr():
    expected_repr = 'MatchUp(2, 256)'
    match_up = MatchUp(2, 256)

    repr_text = repr(match_up)

    assert expected_repr == repr_text


def test_keys():
    expected_keys = {(4, 2),
                     (2, 4),
                     (4, 4),
                     (4, 8),
                     (8, 4),
                     (16, 2),
                     (2, 16),
                     (16, 4),
                     (4, 16),
                     (16, 8),
                     (8, 16)}

    counter = WinCounter(player_levels=[4, 16], opponent_min=2, opponent_max=8)

    assert expected_keys == set(counter.keys())


def test_find_next_matchup():
    expected_p1_iterations = 4
    expected_p2_iterations = 2
    counter = WinCounter(player_levels=[4, 16], opponent_min=2, opponent_max=8)

    match_up = counter.find_next_matchup()

    assert expected_p1_iterations == match_up.p1_iterations
    assert expected_p2_iterations == match_up.p2_iterations


def test_find_next_by_p1_wins():
    expected_p1_iterations = 2
    expected_p2_iterations = 4
    counter = WinCounter(player_levels=[4, 16], opponent_min=2, opponent_max=8)
    counter.find_next_matchup().p1_wins += 1

    match_up = counter.find_next_matchup()

    assert expected_p1_iterations == match_up.p1_iterations
    assert expected_p2_iterations == match_up.p2_iterations


def test_find_next_by_p2_wins():
    expected_p1_iterations = 2
    expected_p2_iterations = 4
    counter = WinCounter(player_levels=[4, 16], opponent_min=2, opponent_max=8)
    counter.find_next_matchup().p2_wins += 1

    match_up = counter.find_next_matchup()

    assert expected_p1_iterations == match_up.p1_iterations
    assert expected_p2_iterations == match_up.p2_iterations


def test_build_series():
    counter = WinCounter(player_levels=[4, 16], opponent_min=2, opponent_max=8)
    counter[(2, 4)].p1_wins = 3
    counter[(2, 4)].p2_wins = 1
    counter[(16, 8)].p1_wins = 4
    counter[(16, 8)].ties = 1
    expected_opponent_levels = [2, 4, 8]
    expected_series = [('wins as 1 with 4', [0., 0., 0.]),
                       ('ties as 1 with 4', [0., 0., 0.]),
                       ('wins as 2 with 4', [0.25, 0., 0.]),
                       ('ties as 2 with 4', [0., 0., 0.]),
                       ('wins as 1 with 16', [0., 0., 0.8]),
                       ('ties as 1 with 16', [0., 0., 0.2]),
                       ('wins as 2 with 16', [0., 0., 0.]),
                       ('ties as 2 with 16', [0., 0., 0.])]

    opponent_levels = counter.opponent_levels
    series = counter.build_series()

    assert expected_opponent_levels == opponent_levels
    assert expected_series == series


def test():
    counter = WinCounter(player_levels=[4, 16], opponent_min=2, opponent_max=8)
    counter[(2, 4)].p1_wins = 3
    counter[(2, 4)].p2_wins = 1
    counter[(16, 8)].p1_wins = 4
    counter[(16, 8)].ties = 1
    expected_summary = """\
opponent levels [2 4 8]
counts as 1 with 4 [0 0 0]
wins as 1 with 4 [0 0 0]
ties as 1 with 4 [0 0 0]
counts as 2 with 4 [4 0 0]
wins as 2 with 4 [25  0  0]
ties as 2 with 4 [0 0 0]
counts as 1 with 16 [0 0 5]
wins as 1 with 16 [ 0  0 80]
ties as 1 with 16 [ 0  0 20]
counts as 2 with 16 [0 0 0]
wins as 2 with 16 [0 0 0]
ties as 2 with 16 [0 0 0]
"""

    summary = counter.build_summary()

    assert expected_summary == summary


def test_copy():
    counter1 = WinCounter(player_levels=[4, 16], opponent_min=2, opponent_max=8)
    counter1[(2, 4)].p1_wins = 3

    counter2 = WinCounter(source=counter1)
    counter1[(16, 8)].p1_wins = 5

    assert 3 == counter2[(2, 4)].p1_wins
    assert 0 == counter2[(16, 8)].p1_wins
