from traceback import print_exc

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QMessageBox

from zero_play.game_state import GameState
from zero_play.mcts_player import MctsPlayer


class MctsWorker(QObject):
    move_chosen = Signal(int)
    # board, analysing_player, [(move_text, probability, count)] for top 10 choices
    move_analysed = Signal(GameState, int, list)

    def __init__(self, player: MctsPlayer, parent: QObject = None):
        super().__init__(parent)
        self.player = player

    @Slot(int, GameState)  # type: ignore
    def choose_move(self, active_player: int, game_state: GameState):
        # noinspection PyBroadException
        try:
            if self.player.player_number != active_player:
                return

            move = self.player.choose_move(game_state)
            # noinspection PyUnresolvedReferences
            self.move_chosen.emit(move)  # type: ignore
        except Exception:
            print_exc()
            message = QMessageBox()
            message.setWindowTitle('Error')
            message.setText(f'Failed to choose a move.')
            message.exec_()

    @Slot(GameState)  # type: ignore
    def analyse_move(self, game_state: GameState):
        move_probabilities = self.player.get_move_probabilities(game_state)
        # noinspection PyUnresolvedReferences
        self.move_analysed.emit(game_state,  # type: ignore
                                self.player.player_number,
                                move_probabilities)
