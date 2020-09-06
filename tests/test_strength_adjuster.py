from zero_play.strength_adjuster import StrengthAdjuster


def test_first_loss():
    strength_adjuster = StrengthAdjuster(strength=1000)
    strength_adjuster.record_score(-1)

    assert strength_adjuster.strength == 500
    assert strength_adjuster.game_count == 1
    assert strength_adjuster.last_score == -1
    assert strength_adjuster.streak_length == 1


def test_first_win():
    strength_adjuster = StrengthAdjuster(strength=1000)
    strength_adjuster.record_score(1)

    assert strength_adjuster.strength == 1500


def test_second_game_win():
    strength_adjuster = StrengthAdjuster(strength=1000,
                                         game_count=1)
    strength_adjuster.record_score(1)

    assert strength_adjuster.strength == 1334


def test_second_win_in_a_row():
    strength_adjuster = StrengthAdjuster(strength=1000,
                                         game_count=1,
                                         last_score=1)
    strength_adjuster.record_score(1)

    assert strength_adjuster.strength == 1667


def test_third_win_in_a_row():
    strength_adjuster = StrengthAdjuster(strength=1000,
                                         game_count=2,
                                         last_score=1,
                                         streak_length=2)
    strength_adjuster.record_score(1)

    assert strength_adjuster.strength == 1750
    assert strength_adjuster.game_count == 3
    assert strength_adjuster.last_score == 1
    assert strength_adjuster.streak_length == 3
