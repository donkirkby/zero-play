import os
import sys
import typing

from PySide2.QtGui import QResizeEvent
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, \
    QGraphicsScene
from pkg_resources import iter_entry_points, EntryPoint

from zero_play.connect4.display import Connect4Display
from zero_play.connect4.game import Connect4Game
from zero_play.game import Game
from zero_play.heuristic import Heuristic
from zero_play.main_window import Ui_MainWindow
from zero_play.othello.game import OthelloGame
from zero_play.plot_canvas import PlotCanvas
from zero_play.tictactoe.display import TicTacToeDisplay
from zero_play.tictactoe.game import TicTacToeGame


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.plot_canvas = PlotCanvas(self.ui.centralwidget)
        self.ui.plot_page.layout().addWidget(self.plot_canvas)
        self.ui.tic_tac_toe.clicked.connect(self.on_tic_tac_toe)
        self.ui.othello.clicked.connect(self.on_othello)
        self.ui.connect4.clicked.connect(self.on_connect4)
        self.ui.network1.clicked.connect(self.on_network1)
        self.ui.cancel.clicked.connect(self.on_cancel)
        self.ui.start.clicked.connect(self.on_start)
        self.ui.action_game.triggered.connect(self.on_new_game)
        self.on_new_game()
        self.ui.display_view.setScene(QGraphicsScene(0, 0, 1, 1))
        self.game = None
        self.display: typing.Optional[TicTacToeDisplay] = None

    def on_new_game(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.game_page)

    def show_game(self, game: Game):
        self.game = game
        self.ui.game_name.setText(game.name)
        heuristics = []
        entry: EntryPoint
        for entry in iter_entry_points('zero_play.heuristic'):
            try:
                heuristic_class = entry.load()
            except ImportError as ex:
                library_path = os.environ.get('LD_LIBRARY_PATH')
                if library_path is not None:
                    raise
                message = (f'Unable to load entry {entry.name}. Do you need to '
                           f'set LD_LIBRARY_PATH?')
                raise ImportError(message) from ex
            try:
                heuristic: Heuristic = heuristic_class(game)
            except ValueError:
                continue
            heuristics.append((entry.name, heuristic))
        self.ui.player1.clear()
        self.ui.player2.clear()
        for name, heuristic in heuristics:
            self.ui.player1.addItem(name, heuristic)
            self.ui.player2.addItem(name, heuristic)

        self.ui.stacked_widget.setCurrentWidget(self.ui.players_page)

    def on_tic_tac_toe(self):
        self.show_game(TicTacToeGame())
        self.display = TicTacToeDisplay(self.ui.display_view.scene())

    def on_othello(self):
        self.show_game(OthelloGame())

    def on_connect4(self):
        self.show_game(Connect4Game())
        self.display = Connect4Display(self.ui.display_view.scene())

    def on_cancel(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.game_page)

    def on_network1(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self.ui.players_page,
            "Open a file for player 1's neural network.",
            filter='Checkpoint (*.h5)',
            options=QFileDialog.DontUseNativeDialog)

    def on_start(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.display_page)
        self.resize_display()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.resize_display()

    def resize_display(self):
        if self.display is None:
            return
        size = self.ui.display_view.maximumViewportSize()
        self.display.resize(size)
        self.display.scene.setSceneRect(0, 0, size.width(), size.height())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
