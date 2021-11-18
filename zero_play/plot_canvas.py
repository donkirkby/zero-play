import matplotlib.pyplot as plt
from PySide6 import QtWidgets

from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from zero_play.game_state import GameState
from zero_play.models import SessionBase
from zero_play.models.game import GameRecord
from zero_play.models.match import MatchRecord
from zero_play.models.match_player import MatchPlayerRecord
from zero_play.tictactoe.state import TicTacToeState

plt.switch_backend('Qt5Agg')


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes: Axes = fig.add_subplot(111)
        self.game: GameState = TicTacToeState()

        super().__init__(fig)
        self.setParent(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.updateGeometry()

    def requery(self, db_session: SessionBase):
        game_record = GameRecord.find_or_create(db_session, self.game)
        strengths = []
        datetimes = []
        match: MatchRecord
        # noinspection PyTypeChecker
        for match in game_record.matches:  # type: ignore
            match_player: MatchPlayerRecord
            # noinspection PyTypeChecker
            for match_player in match.match_players:  # type: ignore
                player = match_player.player
                if player.type != player.HUMAN_TYPE:
                    strengths.append(player.iterations)
                    datetimes.append(match.start_time)

        self.axes.clear()
        self.axes.plot(strengths)
        self.axes.set_ylim(0)
        self.axes.set_title('Search iterations over time')
        self.axes.set_ylabel('Search iterations')
        self.axes.set_xlabel('Number of games played')
        self.axes.figure.canvas.draw()
