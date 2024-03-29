from abc import abstractmethod
import typing

import numpy as np
from PySide6.QtCore import Signal, QThread, QSize, Slot
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QGraphicsSimpleTextItem

from zero_play.game_state import GameState
from zero_play.log_display import LogDisplay
from zero_play.mcts_player import MctsPlayer
from zero_play.mcts_worker import MctsWorker
from zero_play.process_display import ProcessDisplay


class GameDisplay(ProcessDisplay):
    rules_path: typing.Optional[str] = None

    move_needed = Signal(int, np.ndarray)  # active_player, board
    move_made = Signal(np.ndarray)  # board
    game_ended = Signal(np.ndarray)  # final_board

    def __init__(self, start_state: GameState):
        super().__init__()
        self.start_state = start_state
        self.mcts_workers: typing.Dict[int, MctsWorker] = {}
        self.current_state = self.start_state
        self.valid_moves = self.start_state.get_valid_moves()
        self._show_coordinates = False
        self.log_display = LogDisplay()
        self.is_reviewing = False

    @property
    def show_coordinates(self):
        return self._show_coordinates

    @show_coordinates.setter
    def show_coordinates(self, value):
        self._show_coordinates = value
        # noinspection PyUnresolvedReferences
        scene = self.scene()
        size = QSize(scene.width(), scene.height())
        self.resizeEvent(QResizeEvent(size, size))

    @property
    def mcts_players(self):
        return [worker.player for worker in self.mcts_workers.values()]

    @mcts_players.setter
    def mcts_players(self, players: typing.Sequence[MctsPlayer]):
        self.stop_workers()

        self.log_display = LogDisplay()
        self.mcts_workers = {player.player_number: MctsWorker(player)
                             for player in players}
        if not self.mcts_workers:
            self.worker_thread = None
        else:
            self.worker_thread = QThread()
            self.worker_thread.finished.connect(  # type: ignore
                self.worker_thread.deleteLater)
            for worker in self.mcts_workers.values():
                worker.move_chosen.connect(self.make_move)  # type: ignore
                worker.move_analysed.connect(self.analyse_move)  # type: ignore
                self.move_needed.connect(worker.choose_move)  # type: ignore
                self.move_made.connect(worker.analyse_move)  # type: ignore
                worker.moveToThread(self.worker_thread)
            self.worker_thread.start()

    def get_player(self, player_number: int) -> typing.Optional[MctsPlayer]:
        worker = self.mcts_workers.get(player_number)
        if worker:
            return worker.player
        return None

    @abstractmethod
    def update_board(self, board: GameState):
        """ Update self.scene, based on the state in board.

        It's probably also helpful to override resizeEvent().

        :param board: the state of the game to display.
        """

    def resizeEvent(self, event: QResizeEvent):
        self.update_board(self.current_state)

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        """ Return a list of label and detail pairs.

        These are displayed in the about box.
        """
        return ()

    def choose_active_text(self):
        active_player = self.current_state.get_active_player()
        if active_player in self.mcts_workers:
            return 'thinking'
        return 'to move'

    @Slot(int)  # type: ignore
    def make_move(self, move: int):
        self.log_display.record_move(self.current_state, move)
        # noinspection PyUnresolvedReferences
        self.move_made.emit(self.current_state)  # type: ignore
        self.current_state = self.current_state.make_move(move)
        self.update_board(self.current_state)
        if self.current_state.is_ended():
            # noinspection PyUnresolvedReferences
            self.game_ended.emit(self.current_state)  # type: ignore

        forced_move = self.get_forced_move()
        if forced_move is None:
            self.request_move()
        else:
            self.make_move(forced_move)

    def get_forced_move(self) -> typing.Optional[int]:
        """ Override this method if some moves should be forced.

        Look at self.valid_moves and self.current_board to decide.
        :return: move number, or None if there is no forced move.
        """
        return None

    @Slot(GameState, int, list)  # type: ignore
    def analyse_move(
            self,
            board: GameState,
            analysing_player: int,
            move_probabilities: typing.List[typing.Tuple[str,
                                                         float,
                                                         int,
                                                         float]]):
        self.log_display.analyse_move(board,
                                      analysing_player,
                                      move_probabilities)

    def request_move(self):
        if self.current_state.is_ended():
            return
        player = self.current_state.get_active_player()
        # noinspection PyUnresolvedReferences
        self.move_needed.emit(player, self.current_state)

    def can_move(self):
        if self.is_reviewing:
            return False
        return not self.current_state.get_active_player() in self.mcts_workers


def center_text_item(item: QGraphicsSimpleTextItem, x: float, y: float):
    bounds = item.boundingRect()
    x -= bounds.width() // 2
    y -= bounds.height() // 2
    item.setPos(x, y)
