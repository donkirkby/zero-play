from zero_play.log_display import LogDisplay, LogItem
from zero_play.othello.game import OthelloState
from zero_play.tictactoe.state import TicTacToeState


def test_record_move():
    log = LogDisplay()
    step = 1
    move = 3
    board = TicTacToeState()

    log.record_move(board, move)

    assert log.items == [LogItem(step, 'Player X', '2A', board)]


def test_analyse_move():
    log = LogDisplay()
    step = 1
    move = 3
    move_probabilities = [('1A', 0.9, 9, 0.9),
                          ('1B', 0.1, 1, 0.1),
                          ('2A', 0.0, 0, -0.1)]
    board = TicTacToeState()

    log.record_move(board, move)
    log.analyse_move(board, TicTacToeState.X_PLAYER, move_probabilities)

    assert log.items == [
        LogItem(step, 'Player X', '2A', board, 'choice 3', move_probabilities)]


def test_analyse_move_other_player():
    log = LogDisplay()
    step = 1
    move = 3
    move_probabilities = [('1A', 0.8, 8, 0.9),
                          ('1B', 0.1, 1, 0.1),
                          ('2A', 0.1, 1, -0.1)]
    board = TicTacToeState()

    log.record_move(board, move)
    log.analyse_move(board, TicTacToeState.O_PLAYER, move_probabilities)

    assert log.items == [
        LogItem(step, 'Player X', '2A', board, 'choice 3', move_probabilities)]


def test_analyse_move_both_players():
    log = LogDisplay()
    step = 1
    move = 3
    move_probabilities_active_player = [('1A', 0.9, 9, 1.0),
                                        ('1B', 0.1, 1, 0.1),
                                        ('2A', 0.0, 0, 0.0)]
    move_probabilities_other_player = [('1A', 0.8, 8, 0.9),
                                       ('1B', 0.1, 1, 0.1),
                                       ('2A', 0.1, 1, 0.1)]
    board = TicTacToeState()

    log.record_move(board, move)
    log.analyse_move(board,
                     TicTacToeState.O_PLAYER,
                     move_probabilities_other_player)
    log.analyse_move(board,
                     TicTacToeState.X_PLAYER,
                     move_probabilities_active_player)
    log.analyse_move(board,
                     TicTacToeState.O_PLAYER,
                     move_probabilities_other_player)

    assert log.items == [
        LogItem(step,
                'Player X',
                '2A',
                board,
                'choice 3',
                move_probabilities_active_player)]


def test_analyse_best_move():
    log = LogDisplay()
    step = 1
    move = 0
    move_probabilities = [('1A', 0.9, 9, 0.9),
                          ('1B', 0.1, 1, 0.1),
                          ('2A', 0.0, 0, -0.1)]
    board = TicTacToeState()

    log.record_move(board, move)
    log.analyse_move(board, TicTacToeState.X_PLAYER, move_probabilities)

    assert log.items == [
        LogItem(step, 'Player X', '1A', board, '', move_probabilities)]


def test_analyze_bad_move():
    """ Player chooses a move not in the top ten. """
    log = LogDisplay()
    step = 1
    move = 60  # 8E
    move_probabilities = [('2G', 1.0, 9999, 1.0),
                          ('2F', 0.0, 2, 0.0),
                          ('3F', 0.0, 2, 0.0),
                          ('2D', 0.0, 2, 0.0),
                          ('2C', 0.0, 2, 0.0),
                          ('3C', 0.0, 2, 0.0),
                          ('4C', 0.0, 2, 0.0),
                          ('6C', 0.0, 2, 0.0),
                          ('7D', 0.0, 2, 0.0),
                          ('7E', 0.0, 2, 0.0)]
    board = OthelloState("""\
........
........
...XO.X.
...OOXXO
..OXXXXO
...XXXXO
.....XOO
.....OOO
>O
""", board_height=8, board_width=8)

    log.record_move(board, move)
    log.analyse_move(board, TicTacToeState.X_PLAYER, move_probabilities)

    assert log.items == [
        LogItem(step, 'Player O', '8E', board, '?', move_probabilities)]


def test_rewind():
    log = LogDisplay()
    board = TicTacToeState()
    log.record_move(board, 0)
    log.record_move(board, 1)
    log.record_move(board, 2)

    log.rewind_to(2)

    assert len(log.items) == 2
    assert log.step == 2
