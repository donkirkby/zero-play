from PySide2.QtCore import QObject, Signal, Slot

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
        if self.player.player_number != active_player:
            return

        move = self.player.choose_move(game_state)
        # noinspection PyUnresolvedReferences
        self.move_chosen.emit(move)  # type: ignore

    @Slot(GameState)  # type: ignore
    def analyse_move(self, game_state: GameState):
        move_probabilities = self.player.get_move_probabilities(game_state)
        # noinspection PyUnresolvedReferences
        self.move_analysed.emit(game_state,  # type: ignore
                                self.player.player_number,
                                move_probabilities)
