import math
import os
import sys
import typing
from datetime import datetime
from functools import partial
from itertools import chain
from operator import attrgetter
from os import cpu_count
from pathlib import Path
from random import shuffle

import numpy as np
from PySide6.QtCore import QSettings

from PySide6.QtGui import Qt, QIcon, QPixmap
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                               QTableWidgetItem, QGridLayout, QPushButton,
                               QSizePolicy, QDialog, QWidget, QLabel, QComboBox)
from alembic import command
from alembic.config import Config
from pkg_resources import iter_entry_points, EntryPoint
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as BaseSession
from sqlalchemy.util import immutabledict

import zero_play
from zero_play.about_dialog import Ui_Dialog
from zero_play.game_state import GameState
from zero_play.game_display import GameDisplay
from zero_play.main_window import Ui_MainWindow
from zero_play.mcts_player import MctsPlayer
from zero_play.models import Session
from zero_play.models.game import GameRecord
from zero_play.models.match import MatchRecord
from zero_play.models.match_player import MatchPlayerRecord
from zero_play.models.player import PlayerRecord
from zero_play.play_controller import PlayController
from zero_play.playout import Playout
from zero_play.process_display import ProcessDisplay
from zero_play.strength_adjuster import StrengthAdjuster
from zero_play import zero_play_rules_rc
from zero_play import zero_play_images_rc
from zero_play.strength_history_plot import StrengthHistoryPlot
from zero_play.strength_plot import StrengthPlot

assert zero_play_rules_rc  # Need to import this module to load resources.
assert zero_play_images_rc  # Need to import this module to load resources.

try:
    from zero_play.plot_canvas import PlotCanvas
except ImportError:
    from zero_play.plot_canvas_dummy import PlotCanvasDummy as PlotCanvas  # type: ignore

DEFAULT_SEARCHES = 600


class AboutDialog(QDialog):
    def __init__(self,
                 credit_pairs: typing.Iterable[typing.Tuple[str, str]],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.version.setText(zero_play.__version__)
        credits_layout = self.ui.credits_layout
        row = 0
        for row, (title, text) in enumerate(credit_pairs):
            credits_layout.addWidget(QLabel(title),
                                     row,
                                     0,
                                     Qt.AlignmentFlag.AlignRight)
            credits_layout.addWidget(QLabel(text), row, 1)
        row += 1
        credits_layout.addWidget(self.ui.version_label, row, 0)
        credits_layout.addWidget(self.ui.version, row, 1)


def get_settings(game_state: GameState | None = None):
    settings = QSettings("Don Kirkby", "Zero Play")
    if game_state is not None:
        settings.beginGroup('games')
        settings.beginGroup(game_state.game_name.replace(' ', '_'))

    return settings


def get_database_url(database_path: Path | None = None) -> typing.Optional[str]:
    if database_path is None:
        settings = get_settings()
        database_path = settings.value('db_path')
        if database_path is None or not os.path.exists(str(database_path)):
            return None
    database_url = f'sqlite:///{database_path}'
    return database_url


class ZeroPlayWindow(QMainWindow):
    """ Main window for a collection of board games.

    To create your own collection, declare a sub class, and override these
    methods: get_collection_name(), filter_games().
    """
    icon_path = ":/zero_play_images/main_icon.png"

    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        ui = self.ui = Ui_MainWindow()
        ui.setupUi(self)
        self.plot_canvas = StrengthHistoryPlot(ui.centralwidget)
        ui.plot_history_page.layout().addWidget(self.plot_canvas, 1, 0, 1, 2)
        self.strength_canvas = StrengthPlot(ui.centralwidget)
        ui.plot_strength_display_page.layout().addWidget(self.strength_canvas)
        ui.cancel.clicked.connect(self.on_cancel)
        ui.start.clicked.connect(self.on_start)
        ui.action_game.triggered.connect(self.on_new_game)
        ui.action_new_db.triggered.connect(self.on_new_db)
        ui.action_open_db.triggered.connect(self.on_open_db)
        ui.action_plot.triggered.connect(self.on_plot)
        ui.action_coordinates.triggered.connect(self.on_view_coordinates)
        ui.action_about.triggered.connect(self.on_about)
        ui.action_strength_test.triggered.connect(self.on_new_strength_test)
        ui.start_strength_test.clicked.connect(self.on_start_strength_test)
        ui.toggle_review.clicked.connect(self.on_toggle_review)
        ui.resume_here.clicked.connect(self.on_resume_here)
        ui.rules_close.clicked.connect(self.on_close_rules)
        ui.move_history.currentIndexChanged.connect(self.on_move_history)
        ui.player1.currentIndexChanged.connect(
            lambda new_index: self.on_player_changed(ui.player1, new_index))
        ui.player2.currentIndexChanged.connect(
            lambda new_index: self.on_player_changed(ui.player2, new_index))
        ui.searches1.valueChanged.connect(self.on_searches_changed)
        ui.searches_lock1.stateChanged.connect(self.on_lock_changed)
        ui.searches_lock2.stateChanged.connect(self.on_lock_changed)
        self.cpu_count = cpu_count() or 1
        self.is_history_dirty = False  # Has current game been rewound?
        self.all_displays: typing.List[GameDisplay] = []
        self.load_game_list(ui.game_page.layout())
        icon_pixmap = QPixmap(self.icon_path)  # After displays load resources!
        icon = QIcon(icon_pixmap)
        self.setWindowIcon(icon)
        self.start_state: typing.Optional[GameState] = None
        self.display: ProcessDisplay | StrengthPlot | None = None
        self.game_display: typing.Optional[GameDisplay] = None
        self.on_new_game()
        self.board_to_resume: typing.Optional[np.ndarray] = None
        self.review_names = [name.strip()
                             for name in ui.toggle_review.text().split('/')]
        self.are_coordinates_always_visible = False
        self.game_start_time = datetime.now()
        ui.history_game.currentIndexChanged.connect(self.requery_plot)
        self._db_session = None
        settings = get_settings()
        ui.strength_test_game.setCurrentText(settings.value(
            'strength_test_game',
            ui.strength_test_game.currentText()))
        ui.strength_test_strengths.setText(settings.value(
            'strength_test_strengths',
            ui.strength_test_strengths.text()))
        ui.strength_test_min.setValue(settings.value(
            'strength_test_min',
            ui.strength_test_min.value(),
            type=int))
        ui.strength_test_max.setValue(settings.value(
            'strength_test_max',
            ui.strength_test_max.value(),
            type=int))
        self.on_toggle_review()

    @staticmethod
    def get_collection_name() -> str:
        return 'Zero Play'

    @staticmethod
    def filter_games(
            entries: typing.Iterable[EntryPoint]) -> typing.Generator[EntryPoint,
                                                                      None,
                                                                      None]:
        yield from entries

    @property
    def db_session(self) -> typing.Optional[BaseSession]:
        if self._db_session is None:
            db_url = get_database_url()
            if db_url is None:
                return None
            engine = create_engine(db_url)
            Session.configure(bind=engine)
            self._db_session = Session()
        return self._db_session

    def on_about(self):
        credit_pairs = chain(*(display.credit_pairs
                               for display in self.all_displays))
        dialog = AboutDialog(credit_pairs, self)
        dialog.setWindowTitle(f'About {self.get_collection_name()}')
        dialog.exec_()

    def load_game_list(self, game_layout: QGridLayout):
        while game_layout.count():
            child = game_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        games = self.all_displays
        all_entries = iter_entry_points('zero_play.game_display')
        filtered_entries = self.filter_games(all_entries)
        for game_entry in filtered_entries:
            display_class = game_entry.load()
            display: GameDisplay = display_class()
            self.destroyed.connect(display.close)  # type: ignore
            display.game_ended.connect(self.on_game_ended)  # type: ignore
            games.append(display)
        games.sort(key=attrgetter('start_state.game_name'))
        column_count = math.ceil(math.sqrt(len(games)))
        for i, display in enumerate(games):
            row = i // column_count
            column = i % column_count
            game_name = display.start_state.game_name
            game_button = QPushButton(game_name)
            game_button.setSizePolicy(QSizePolicy.Policy.Minimum,
                                      QSizePolicy.Policy.Minimum)

            game_button.clicked.connect(partial(self.show_game,  # type: ignore
                                                display))
            game_layout.addWidget(game_button, row, column)

            self.ui.history_game.addItem(game_name, userData=display)
            self.ui.strength_test_game.addItem(game_name, userData=display)

            if display.rules_path is not None:
                game_rules_action = self.ui.menu_rules.addAction(game_name)
                game_rules_action.triggered.connect(partial(self.on_rules,
                                                            display))

    def on_toggle_review(self):
        choices = self.ui.choices
        current_page = self.ui.stacked_widget.currentWidget()
        is_game_displayed = current_page is self.ui.display_page
        is_named_review = self.ui.toggle_review.text() == self.review_names[0]
        is_review_visible = is_game_displayed and is_named_review
        if not is_review_visible:
            if self.game_display is not None and self.board_to_resume is not None:
                self.game_display.update_board(self.board_to_resume)
            self.board_to_resume = None
            self.ui.action_coordinates.setChecked(
                self.are_coordinates_always_visible)
            self.on_view_coordinates(self.are_coordinates_always_visible)
        else:
            self.board_to_resume = self.game_display.current_state
            self.are_coordinates_always_visible = (
                self.ui.action_coordinates.isChecked())
            self.ui.action_coordinates.setChecked(True)
            self.on_view_coordinates(True)
            choices.clear()
            choices.setRowCount(3)
            choices.setColumnCount(10)
            choices.resizeColumnsToContents()
            choices.resizeRowsToContents()
            choices.setMaximumHeight(choices.horizontalHeader().height() +
                                     choices.verticalHeader().length() +
                                     choices.horizontalScrollBar().height())
            self.ui.move_history.clear()
            self.ui.move_history.addItems(
                [str(item) for item in self.game_display.log_display.items])
            self.ui.move_history.setCurrentIndex(self.ui.move_history.count()-1)

        self.ui.resume_here.setVisible(is_review_visible)
        self.ui.move_history.setVisible(is_review_visible)
        self.ui.choices.setVisible(is_review_visible)
        self.ui.toggle_review.setText(self.review_names[is_review_visible])
        if self.game_display is not None:
            self.game_display.is_reviewing = is_review_visible
        choices.setVisible(is_review_visible)

    def on_resume_here(self):
        self.board_to_resume = self.game_display.current_state
        self.is_history_dirty = True
        history_index = self.ui.move_history.currentIndex()
        self.game_display.log_display.rewind_to(history_index)
        self.on_toggle_review()
        self.game_display.request_move()

    def on_move_history(self, item_index: int):
        assert self.game_display is not None
        history_item = self.game_display.log_display.items[item_index]
        self.game_display.update_board(history_item.game_state)
        choices = self.ui.choices
        choices.clear()
        choices.setColumnCount(len(history_item.choices))
        choices.setVerticalHeaderLabels(['count', 'probability', 'value'])
        choices.setHorizontalHeaderLabels([choice[0]
                                           for choice in history_item.choices])
        for i, (choice,
                probability,
                count,
                value) in enumerate(history_item.choices):
            choices.setItem(0, i, QTableWidgetItem(f'{count}'))
            choices.setItem(1, i, QTableWidgetItem(f'{probability}'))
            choices.setItem(2, i, QTableWidgetItem(f'{value}'))
        choices.resizeColumnsToContents()

    def on_new_game(self):
        self.stop_workers()
        self.ui.stacked_widget.setCurrentWidget(self.ui.game_page)
        self.setWindowTitle(self.get_collection_name())

    def stop_workers(self):
        if self.display is not None:
            self.display.stop_workers()
            self.display = self.game_display = None

    def show_game(self, display: GameDisplay):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.display = self.game_display = display
        start_state = display.start_state
        self.start_state = start_state
        collection_name = self.get_collection_name()
        self.setWindowTitle(f'{collection_name} - {start_state.game_name}')
        self.ui.game_name.setText(start_state.game_name)
        settings = get_settings(start_state)
        is_locked = settings.value('searches_locked', False, bool)
        self.ui.searches_lock1.setChecked(is_locked)
        self.ui.searches_lock2.setChecked(is_locked)
        search_count = settings.value('searches', DEFAULT_SEARCHES, int)
        self.ui.searches1.setValue(search_count)
        self.ui.searches2.setValue(search_count)
        self.ui.shuffle_players.setChecked(settings.value('shuffle_players',
                                                          False,
                                                          bool))
        heuristics = self.load_heuristics()
        player1_index = settings.value('player_1', 0, int)
        player2_index = settings.value('player_2', 0, int)
        self.ui.player1.clear()
        self.ui.player2.clear()
        self.ui.player1.addItem('Human', None)
        self.ui.player2.addItem('Human', None)
        for name, heuristic in heuristics:
            self.ui.player1.addItem(name, heuristic)
            self.ui.player2.addItem(name, heuristic)

        self.ui.player1.setCurrentIndex(player1_index)
        self.ui.player2.setCurrentIndex(player2_index)
        self.ui.stacked_widget.setCurrentWidget(self.ui.players_page)
        self.board_to_resume = None
        self.on_toggle_review()
        QApplication.restoreOverrideCursor()

    def on_player_changed(self, player: QComboBox, new_index: int):
        if new_index < 0:
            # Combo box was cleared.
            return
        assert self.start_state is not None
        settings = get_settings(self.start_state)
        if player is self.ui.player1:
            searches = self.ui.searches1
            searches_label = self.ui.searches_label1
            searches_lock = self.ui.searches_lock1
            setting_name = 'player_1'
            row = 1
        else:
            searches = self.ui.searches2
            searches_label = self.ui.searches_label2
            searches_lock = self.ui.searches_lock2
            setting_name = 'player_2'
            row = 2
        settings.setValue(setting_name, new_index)
        heuristic = player.itemData(new_index)
        searches.setVisible(heuristic is not None)
        searches_label.setVisible(heuristic is not None)
        searches_lock.setVisible(heuristic is not None)
        colspan = 4 if heuristic is None else 1
        self.ui.player_layout.addWidget(player, row, 1, 1, colspan)

    @staticmethod
    def load_heuristics():
        heuristics = [('Computer', Playout())]
        # entry: EntryPoint
        # for entry in iter_entry_points('zero_play.heuristic'):
        #     try:
        #         heuristic_class = entry.load()
        #     except ImportError as ex:
        #         library_path = os.environ.get('LD_LIBRARY_PATH')
        #         if library_path is not None:
        #             raise
        #         message = (f'Unable to load entry {entry.name}. Do you need to'
        #                    f' set LD_LIBRARY_PATH?')
        #         raise ImportError(message) from ex
        #     try:
        #         heuristic: Heuristic = heuristic_class(start_state)
        #     except ValueError:
        #         continue
        #     heuristics.append((entry.name, heuristic))
        return heuristics

    def on_cancel(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.game_page)

    def on_network1(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self.ui.players_page,
            "Open a file for player 1's neural network.",
            filter='Checkpoint (*.h5)',
            options=QFileDialog.DontUseNativeDialog)

    def on_start(self) -> None:
        self.game_start_time = datetime.now()
        assert self.game_display is not None
        assert self.start_state is not None
        self.game_display.update_board(self.game_display.start_state)
        self.is_history_dirty = False
        ui = self.ui
        player_fields = [(ui.player1.currentData(), ui.searches1.value()),
                         (ui.player2.currentData(), ui.searches2.value())]
        is_shuffled = ui.shuffle_players.isChecked()
        settings = get_settings(self.start_state)
        settings.setValue('shuffle_players', is_shuffled)
        if is_shuffled:
            shuffle(player_fields)
        mcts_choices = {self.start_state.players[0]: player_fields[0],
                        self.start_state.players[1]: player_fields[1]}
        self.game_display.mcts_players = [
            MctsPlayer(self.start_state,
                       player_number,
                       iteration_count=searches,
                       process_count=self.cpu_count)
            for player_number, (heuristic, searches) in mcts_choices.items()
            if heuristic is not None]
        layout: QGridLayout = ui.display_page.layout()
        layout.replaceWidget(ui.game_display, self.game_display)
        ui.game_display.setVisible(False)
        ui.game_display = self.game_display
        self.game_display.setVisible(True)
        self.game_display.show_coordinates = ui.action_coordinates.isChecked()

        self.on_view_game()

    def on_view_game(self):
        if self.game_display is None:
            self.on_new_game()
        else:
            self.ui.stacked_widget.setCurrentWidget(self.ui.display_page)
            self.game_display.update_board(self.game_display.current_state)
            self.game_display.request_move()

    def on_view_coordinates(self, is_checked: bool):
        if self.game_display is not None:
            self.game_display.show_coordinates = is_checked

    def on_new_strength_test(self):
        self.stop_workers()
        self.ui.stacked_widget.setCurrentWidget(
            self.ui.plot_strength_page)

    def on_start_strength_test(self) -> None:
        settings = get_settings()
        ui = self.ui
        settings.setValue('strength_test_game',
                          ui.strength_test_game.currentText())
        settings.setValue('strength_test_strengths',
                          ui.strength_test_strengths.text())
        settings.setValue('strength_test_min', ui.strength_test_min.value())
        settings.setValue('strength_test_max', ui.strength_test_max.value())
        game_display: GameDisplay = ui.strength_test_game.currentData()
        start_state = game_display.start_state
        players = [MctsPlayer(start_state, GameState.X_PLAYER),
                   MctsPlayer(start_state, GameState.O_PLAYER)]
        controller = PlayController(start_state, players)
        player_definitions = ui.strength_test_strengths.text().split()
        self.display = self.strength_canvas
        assert self.db_session is not None
        self.strength_canvas.start(self.db_session,
                                   controller,
                                   player_definitions,
                                   ui.strength_test_min.value(),
                                   ui.strength_test_max.value())
        ui.stacked_widget.setCurrentWidget(
            ui.plot_strength_display_page)

    def on_plot(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.plot_history_page)
        self.requery_plot()

    def requery_plot(self) -> None:
        display: GameDisplay = self.ui.history_game.currentData()
        self.plot_canvas.game = display.start_state
        settings = get_settings(display.start_state)
        future_strength = settings.value('searches', DEFAULT_SEARCHES, int)
        self.plot_canvas.requery(self.db_session, future_strength)

    def on_searches_changed(self, search_count: int):
        if self.ui.stacked_widget.currentWidget() is not self.ui.players_page:
            return
        if self.start_state is not None:
            settings = get_settings(self.start_state)
            settings.setValue('searches', search_count)
            settings.remove('game_count')
            settings.remove('last_score')
            settings.remove('streak_length')

    def on_game_ended(self, game_state: GameState):
        if (self.is_history_dirty or
                self.game_display is None or
                self.ui.searches_lock1.isChecked()):
            return
        db_session = self.db_session
        if db_session is None:
            return
        game_record = GameRecord.find_or_create(db_session, game_state)
        game_end_time = datetime.now()
        game_duration = game_end_time - self.game_start_time
        match_record = MatchRecord(game=game_record,
                                   start_time=self.game_start_time,
                                   total_seconds=round(game_duration.total_seconds()),
                                   move_count=game_state.get_move_count())
        db_session.add(match_record)
        winner = game_state.get_winner()
        mcts_player: typing.Optional[MctsPlayer]
        for player_number in game_state.get_players():
            mcts_player = self.game_display.get_player(player_number)
            if mcts_player is None:
                player_record = db_session.query(PlayerRecord).filter_by(
                    type=PlayerRecord.HUMAN_TYPE).one_or_none()
                if player_record is None:
                    player_record = PlayerRecord(type=PlayerRecord.HUMAN_TYPE)
                    db_session.add(player_record)
            else:
                player_record = db_session.query(PlayerRecord).filter_by(
                    type=PlayerRecord.PLAYOUT_TYPE,
                    iterations=mcts_player.iteration_count).one_or_none()
                if player_record is None:
                    player_record = PlayerRecord(type=PlayerRecord.PLAYOUT_TYPE,
                                                 iterations=mcts_player.iteration_count)
                    db_session.add(player_record)
            if player_number == winner:
                result = 1
            elif winner == game_state.NO_PLAYER:
                result = 0
            else:
                result = -1
            match_player = MatchPlayerRecord(match=match_record,
                                             player=player_record,
                                             player_number=player_number,
                                             result=result)
            db_session.add(match_player)
        db_session.commit()
        try:
            mcts_player, = self.game_display.mcts_players
        except ValueError:
            # Didn't have exactly one MCTS player
            return
        assert mcts_player is not None
        winning_player = game_state.get_winner()
        if winning_player == mcts_player.player_number:
            score = -1
        elif winning_player == GameState.NO_PLAYER:
            score = 0
        else:
            score = 1
        settings = get_settings(self.start_state)
        strength_adjuster = StrengthAdjuster(
            strength=mcts_player.iteration_count,
            game_count=settings.value('game_count', 0, int),
            last_score=settings.value('last_score', 0, int),
            streak_length=settings.value('streak_length', 1, int))
        strength_adjuster.record_score(score)
        settings.setValue('searches', strength_adjuster.strength)
        settings.setValue('game_count', strength_adjuster.game_count)
        settings.setValue('last_score', strength_adjuster.last_score)
        settings.setValue('streak_length', strength_adjuster.streak_length)

    def on_lock_changed(self, is_checked):
        self.ui.searches_lock1.setChecked(is_checked)
        self.ui.searches_lock2.setChecked(is_checked)
        settings = get_settings(self.start_state)
        settings.setValue('searches_locked', is_checked)

    def on_rules(self, display: GameDisplay):
        self.ui.stacked_widget.setCurrentWidget(self.ui.rules_page)
        rules_path = display.rules_path
        if rules_path is None:
            game_name = display.start_state.game_name
            rules_html = f'No rules found for {game_name}.'
            self.ui.rules_text.setHtml(rules_html)
        else:
            self.ui.rules_text.setSource('qrc' + rules_path)

    def on_close_rules(self):
        if self.game_display is None:
            page = self.ui.game_page
        elif self.game_display.current_state == self.game_display.start_state:
            page = self.ui.players_page
        else:
            page = self.ui.display_page
        self.ui.stacked_widget.setCurrentWidget(page)

    def on_new_db(self):
        settings = get_settings()
        db_path = settings.value('db_path')
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Create a new database",
            dir=db_path,
            filter='Player databases (*.zpl)',
            options=QFileDialog.DontUseNativeDialog)
        if not file_name:
            return
        script_path = str(Path(__file__).parent / 'db')
        database_path = Path(file_name).absolute()
        settings.setValue('db_path', str(database_path))
        database_url = get_database_url(database_path)
        alembic_config = Config(config_args=immutabledict({
            'script_location': script_path,
            'sqlalchemy.url': database_url}))
        command.upgrade(alembic_config, 'head')

    def on_open_db(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = ZeroPlayWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
