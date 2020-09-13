from zero_play.log_display import LogDisplay, LogItem
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


def test_rewind():
    log = LogDisplay()
    board = TicTacToeState()
    log.record_move(board, 0)
    log.record_move(board, 1)
    log.record_move(board, 2)

    log.rewind_to(2)

    assert len(log.items) == 2
    assert log.step == 2
