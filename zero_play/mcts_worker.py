import numpy as np
from PySide2.QtCore import QObject, Signal, Slot

from zero_play.mcts_player import MctsPlayer


class MctsWorker(QObject):
    move_chosen = Signal(int)

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
