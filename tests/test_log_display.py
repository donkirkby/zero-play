from zero_play.log_display import LogDisplay
from zero_play.tictactoe.game import TicTacToeGame


def test_record_move():
    game = TicTacToeGame()
    log = LogDisplay(game)
    move = 1
    move_probabilities = [('1A', 0.9), ('1B', 0.1), ('2B', 0.0)]
    expected_log = """\
event,step,player,move,comment,choice1,prob1,choice2,prob2,choice3,prob3,choice4,prob4,\
choice5,prob5,choice6,prob6,choice7,prob7,choice8,prob8,choice9,prob9,choice10,prob10
move,1,Player X,1B,choice 2,1A,0.9,1B,0.1,2B,0.0,,,,,,,,,,,,,,
"""

    log.record_move(game.create_board(), move, move_probabilities)

    assert log.file.getvalue() == expected_log
