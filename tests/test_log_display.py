from zero_play.log_display import LogDisplay, LogItem
from zero_play.tictactoe.game import TicTacToeGame


def test_record_move():
    game = TicTacToeGame()
    log = LogDisplay(game)
    step = 1
    move = 3
    board = game.create_board()

    log.record_move(board, move)

    assert log.items == [LogItem(step, 'Player X', '2A', board)]


def test_analyse_move():
    game = TicTacToeGame()
    log = LogDisplay(game)
    step = 1
    move = 3
    move_probabilities = [('1A', 0.9, 9, 0.9),
                          ('1B', 0.1, 1, 0.1),
                          ('2A', 0.0, 0, -0.1)]
    board = game.create_board()

    log.record_move(board, move)
    log.analyse_move(board, TicTacToeGame.X_PLAYER, move_probabilities)

    assert log.items == [
        LogItem(step, 'Player X', '2A', board, 'choice 3', move_probabilities)]


def test_analyse_move_other_player():
    game = TicTacToeGame()
    log = LogDisplay(game)
    step = 1
    move = 3
    move_probabilities = [('1A', 0.8, 8, 0.9),
                          ('1B', 0.1, 1, 0.1),
                          ('2A', 0.1, 1, -0.1)]
    board = game.create_board()

    log.record_move(board, move)
    log.analyse_move(board, TicTacToeGame.O_PLAYER, move_probabilities)

    assert log.items == [
        LogItem(step, 'Player X', '2A', board, 'choice 3', move_probabilities)]


def test_analyse_move_both_players():
    game = TicTacToeGame()
    log = LogDisplay(game)
    step = 1
    move = 3
    move_probabilities_active_player = [('1A', 0.9, 9, 1.0),
                                        ('1B', 0.1, 1, 0.1),
                                        ('2A', 0.0, 0, 0.0)]
    move_probabilities_other_player = [('1A', 0.8, 8, 0.9),
                                       ('1B', 0.1, 1, 0.1),
                                       ('2A', 0.1, 1, 0.1)]
    board = game.create_board()

    log.record_move(board, move)
    log.analyse_move(board,
                     TicTacToeGame.O_PLAYER,
                     move_probabilities_other_player)
    log.analyse_move(board,
                     TicTacToeGame.X_PLAYER,
                     move_probabilities_active_player)
    log.analyse_move(board,
                     TicTacToeGame.O_PLAYER,
                     move_probabilities_other_player)

    assert log.items == [
        LogItem(step,
                'Player X',
                '2A',
                board,
                'choice 3',
                move_probabilities_active_player)]
