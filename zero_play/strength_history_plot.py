from zero_play.game_state import GameState
from zero_play.models import SessionBase
from zero_play.models.game import GameRecord
from zero_play.models.match import MatchRecord
from zero_play.models.match_player import MatchPlayerRecord
from zero_play.plot_canvas import PlotCanvas
from zero_play.tictactoe.state import TicTacToeState


class StrengthHistoryPlot(PlotCanvas):
    def __init__(self, parent=None):
        self.game: GameState = TicTacToeState()

        super().__init__(parent)

    def fetch_strengths(self, db_session):
        if db_session is None:
            return []
        game_record = GameRecord.find_or_create(db_session, self.game)
        strengths = []
        match: MatchRecord
        # noinspection PyTypeChecker
        for match in game_record.matches:  # type: ignore
            match_player: MatchPlayerRecord
            has_human = False
            ai_player = None
            # noinspection PyTypeChecker
            for match_player in match.match_players:  # type: ignore
                player = match_player.player
                if player.type == player.HUMAN_TYPE:
                    has_human = True
                else:
                    ai_player = player
            if has_human and ai_player is not None:
                strengths.append(ai_player.iterations)
        return strengths

    def requery(self, db_session: SessionBase | None, future_strength: int):
        strengths = self.fetch_strengths(db_session)

        self.axes.clear()
        marker = 'o' if len(strengths) == 1 else ''
        self.axes.plot(strengths, marker, label='past')
        self.axes.plot([len(strengths)], [future_strength], 'o', label='next')
        self.axes.set_ylim(0)
        if len(strengths) + 1 < len(self.axes.get_xticks()):
            self.axes.set_xticks(list(range(len(strengths) + 1)))
        self.axes.set_title('Search iterations over time')
        self.axes.set_ylabel('Search iterations')
        self.axes.set_xlabel('Number of games played')
        self.axes.legend(loc='lower right')
        self.axes.figure.canvas.draw()
