import numpy as np
from PySide2.QtCore import QObject, Signal, Slot

from zero_play.mcts_player import MctsPlayer


class MctsWorker(QObject):
    move_chosen = Signal(int)
    # board, analysing_player, [(move_text, probability)] for top 10 choices
    move_analysed = Signal(np.ndarray, int, list)

    def __init__(self, player: MctsPlayer, parent: QObject = None):
        super().__init__(parent)
        self.player = player

    @Slot(int, np.ndarray)  # type: ignore
    def choose_move(self, active_player: int, board: np.ndarray):
        if self.player.player_number != active_player:
            return

        move = self.player.choose_move(board)
        # noinspection PyUnresolvedReferences
        self.move_chosen.emit(move)  # type: ignore

    @Slot(np.ndarray)  # type: ignore
    def analyse_move(self, board):
        move_probabilities = self.player.get_move_probabilities(board)
        # noinspection PyUnresolvedReferences
        self.move_analysed.emit(board,
                                self.player.player_number,
                                move_probabilities)
