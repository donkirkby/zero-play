import math
import sys
import typing
from functools import partial
from itertools import chain
from operator import attrgetter

import numpy as np
from PySide2.QtCore import QSettings

from PySide2.QtGui import QResizeEvent, Qt
from PySide2.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                               QTableWidgetItem, QGridLayout, QPushButton,
                               QSizePolicy, QDialog, QWidget, QLabel, QComboBox)
from pkg_resources import iter_entry_points

import zero_play
from zero_play.about_dialog import Ui_Dialog
from zero_play.game import Game
from zero_play.game_display import GameDisplay
from zero_play.grid_display import GridDisplay
from zero_play.main_window import Ui_MainWindow
from zero_play.mcts_player import MctsPlayer
from zero_play.playout import Playout
from zero_play.strength_adjuster import StrengthAdjuster

try:
    from zero_play.plot_canvas import PlotCanvas
except ImportError:
    from zero_play.plot_canvas_dummy import PlotCanvasDummy as PlotCanvas  # type: ignore


class AboutDialog(QDialog):
    def __init__(self,
                 credit_pairs: typing.Iterable[typing.Tuple[str, str]],
                 parent: QWidget = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.version.setText(zero_play.__version__)
        credits_layout = self.ui.credits_layout
        for title, text in credit_pairs:
            row = credits_layout.rowCount()
            credits_layout.addWidget(QLabel(title), row, 0, Qt.AlignRight)
            credits_layout.addWidget(QLabel(text), row, 1)


def get_settings(game: Game = None):
    settings = QSettings("Don Kirkby", "Zero Play")
    if game is not None:
        settings.beginGroup('games')
        settings.beginGroup(game.name.replace(' ', '_'))

    return settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.plot_canvas = PlotCanvas(self.ui.centralwidget)
        self.ui.plot_page.layout().addWidget(self.plot_canvas)
        self.ui.cancel.clicked.connect(self.on_cancel)
        self.ui.start.clicked.connect(self.on_start)
        self.ui.action_game.triggered.connect(self.on_new_game)
        self.ui.action_plot.triggered.connect(self.on_plot)
        self.ui.action_coordinates.triggered.connect(self.on_view_coordinates)
        self.ui.action_about.triggered.connect(self.on_about)
        self.ui.toggle_review.clicked.connect(self.on_toggle_review)
        self.ui.move_history.currentIndexChanged.connect(self.on_move_history)
        self.ui.player1.currentIndexChanged.connect(
            lambda new_index: self.on_player_changed(self.ui.player1, new_index))
        self.ui.player2.currentIndexChanged.connect(
            lambda new_index: self.on_player_changed(self.ui.player2, new_index))
        self.ui.searches1.valueChanged.connect(self.on_searches_changed)
        self.ui.searches_lock1.stateChanged.connect(self.on_lock_changed)
        self.ui.searches_lock2.stateChanged.connect(self.on_lock_changed)
        self.all_displays = []
        self.load_game_list(self.ui.game_page.layout())
        self.game = None
        self.display: typing.Optional[GridDisplay] = None
        self.on_new_game()
        self.board_to_resume: typing.Optional[np.ndarray] = None
        self.review_names = [name.strip()
                             for name in self.ui.toggle_review.text().split('/')]
        self.are_coordinates_always_visible = False
        self.on_toggle_review()

    def on_about(self):
        credit_pairs = chain(*(display.credit_pairs
                               for display in self.all_displays))
        dialog = AboutDialog(credit_pairs, self)
        dialog.exec_()

    def load_game_list(self, game_layout: QGridLayout):
        while game_layout.count():
            child = game_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        games = self.all_displays
        for game_entry in iter_entry_points('zero_play.game_display'):
            display_class = game_entry.load()
            display: GameDisplay = display_class()
            self.destroyed.connect(display.close)
            display.game_ended.connect(self.on_game_ended)  # type: ignore
            games.append(display)
        games.sort(key=attrgetter('game.name'))
        column_count = math.ceil(math.sqrt(len(games)))
        for i, display in enumerate(games):
            row = i // column_count
            column = i % column_count
            game_button = QPushButton(display.game.name)
            game_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            # noinspection PyUnresolvedReferences
            game_button.clicked.connect(partial(self.show_game, display))
            game_layout.addWidget(game_button, row, column)

    def on_toggle_review(self):
        choices = self.ui.choices
        is_review_visible = self.ui.toggle_review.text() == self.review_names[0]
        if not is_review_visible:
            if self.display is not None:
                self.display.update_board(self.board_to_resume)
            self.board_to_resume = None
            self.ui.action_coordinates.setChecked(
                self.are_coordinates_always_visible)
            self.on_view_coordinates(self.are_coordinates_always_visible)
        else:
            self.board_to_resume = self.display.current_board
            self.are_coordinates_always_visible = (
                self.ui.action_coordinates.isChecked())
            self.ui.action_coordinates.setChecked(True)
            self.on_view_coordinates(True)
            choices.clear()
            choices.setRowCount(1)
            choices.setColumnCount(20)
            choices.resizeColumnsToContents()
            choices.resizeRowsToContents()
            choices.setMaximumHeight(choices.horizontalHeader().height() +
                                     choices.verticalHeader().length() +
                                     choices.horizontalScrollBar().height())
            self.ui.move_history.clear()
            self.ui.move_history.addItems(
                [str(item) for item in self.display.log_display.items])
            self.ui.move_history.setCurrentIndex(self.ui.move_history.count()-1)

        self.ui.resume_here.setVisible(is_review_visible)
        self.ui.move_history.setVisible(is_review_visible)
        self.ui.choices.setVisible(is_review_visible)
        self.ui.toggle_review.setText(self.review_names[is_review_visible])
        self.ui.resume_here.setVisible(False)  # Not implemented yet.
        choices.setVisible(is_review_visible)
        self.resize_display()

    def on_move_history(self, item_index: int):
        assert self.display is not None
        history_item = self.display.log_display.items[item_index]
        self.display.update_board(history_item.board)
        self.ui.choices.clear()
        for i, (choice, probability) in enumerate(history_item.choices):
            self.ui.choices.setItem(0, 2*i, QTableWidgetItem(choice))
            self.ui.choices.setItem(0, 2*i+1, QTableWidgetItem(f'{probability}'))
        self.ui.choices.resizeColumnsToContents()

    def on_new_game(self):
        if self.display is not None:
            self.display.close()
            self.display = None
        self.ui.stacked_widget.setCurrentWidget(self.ui.game_page)
        self.ui.action_view_game.setChecked(True)
        self.setWindowTitle('ZeroPlay')

    def show_game(self, display: GameDisplay):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.display = display
        game = display.game
        self.game = game
        self.setWindowTitle(f'ZeroPlay - {game.name}')
        self.ui.game_name.setText(game.name)
        settings = get_settings(game)
        is_locked = settings.value('searches_locked', False, bool)
        self.ui.searches_lock1.setChecked(is_locked)
        self.ui.searches_lock2.setChecked(is_locked)
        search_count = settings.value('searches', 600, int)
        self.ui.searches1.setValue(search_count)
        self.ui.searches2.setValue(search_count)
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
        QApplication.restoreOverrideCursor()

    def on_player_changed(self, player: QComboBox, new_index: int):
        if new_index < 0:
            # Combo box was cleared.
            return
        settings = get_settings(self.game)
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

    def load_heuristics(self):
        game = self.game
        heuristics = [('Computer', Playout(game))]
        # entry: EntryPoint
        # for entry in iter_entry_points('zero_play.heuristic'):
        #     try:
        #         heuristic_class = entry.load()
        #     except ImportError as ex:
        #         library_path = os.environ.get('LD_LIBRARY_PATH')
        #         if library_path is not None:
        #             raise
        #         message = (f'Unable to load entry {entry.name}. Do you need to '
        #                    f'set LD_LIBRARY_PATH?')
        #         raise ImportError(message) from ex
        #     try:
        #         heuristic: Heuristic = heuristic_class(game)
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

    def on_start(self):
        self.display.update_board(self.display.game.create_board())
        mcts_choices = {self.game.X_PLAYER: (self.ui.player1.currentData(),
                                             self.ui.searches1.value()),
                        self.game.O_PLAYER: (self.ui.player2.currentData(),
                                             self.ui.searches2.value())}
        self.display.mcts_players = [
            MctsPlayer(self.game, player_number, iteration_count=searches)
            for player_number, (heuristic, searches) in mcts_choices.items()
            if heuristic is not None]
        layout: QGridLayout = self.ui.display_page.layout()
        layout.removeWidget(self.ui.display_view)
        self.ui.display_view.setVisible(False)
        self.display.setVisible(True)
        self.ui.display_view = self.display
        layout.addWidget(self.display, 0, 0, 1, 3)
        self.display.show_coordinates = self.ui.action_coordinates.isChecked()

        self.on_view_game()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.resize_display()

    def resize_display(self):
        if self.display is None:
            return
        size = self.ui.display_view.maximumViewportSize()
        self.display.resize(size)

    def on_view_game(self):
        if self.display is None:
            self.on_new_game()
        else:
            self.ui.stacked_widget.setCurrentWidget(self.ui.display_page)
            self.resize_display()
            self.display.update_board(self.display.current_board)
            self.display.request_move()

    def on_view_coordinates(self, is_checked: bool):
        if self.display is not None:
            self.display.show_coordinates = is_checked

    def on_plot(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.plot_page)

    def on_searches_changed(self, search_count: int):
        if self.ui.stacked_widget.currentWidget() is not self.ui.players_page:
            return
        if self.game is not None:
            settings = get_settings(self.game)
            settings.setValue('searches', search_count)
            settings.remove('game_count')
            settings.remove('last_score')
            settings.remove('streak_length')

    def on_game_ended(self, board: np.ndarray):
        if self.ui.searches_lock1.isChecked():
            return
        if self.display is None:
            return
        try:
            mcts_player: MctsPlayer
            mcts_player, = self.display.mcts_players
        except ValueError:
            # Didn't have exactly one MCTS player
            return
        winning_player = self.game.get_winner(board)
        if winning_player == mcts_player.player_number:
            score = -1
        elif winning_player == Game.NO_PLAYER:
            score = 0
        else:
            score = 1
        settings = get_settings(self.game)
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
        settings = get_settings(self.game)
        settings.setValue('searches_locked', is_checked)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
