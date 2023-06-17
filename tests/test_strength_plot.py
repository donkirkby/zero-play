from textwrap import dedent

import pytest
from PySide6.QtGui import QPainter
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from sqlalchemy import create_engine

from tests.conftest import paint_figure
from zero_play.models import SessionBase, Session, Base
from zero_play.models.game import GameRecord
from zero_play.models.match import MatchRecord
from zero_play.models.match_player import MatchPlayerRecord
from zero_play.models.player import PlayerRecord
from zero_play.pixmap_differ import PixmapDiffer
from zero_play.strength_plot import StrengthPlot, WinCounter, MatchUp
from zero_play.tictactoe.state import TicTacToeState


# noinspection DuplicatedCode
@pytest.fixture
def memory_db(qapp) -> SessionBase:
    # Open DB and create tables.
    engine = create_engine('sqlite://')
    Session.configure(bind=engine)
    db_session = Session()
    Base.metadata.create_all(engine)

    # Create some test data.
    tic_tac_toe = GameRecord.find_or_create(db_session, TicTacToeState())
    player1 = PlayerRecord(milliseconds=16_000,
                           name='Mr. Strong',
                           type=PlayerRecord.PLAYOUT_TYPE)
    player2 = PlayerRecord(milliseconds=1_000,
                           name='Mr. Weak',
                           type=PlayerRecord.PLAYOUT_TYPE)
    db_session.add(player1)
    db_session.add(player2)
    for i in range(2):
        match = MatchRecord(game=tic_tac_toe)
        db_session.add(match)
        db_session.add(MatchPlayerRecord(match=match,
                                         player=player1,
                                         player_number=TicTacToeState.X_PLAYER,
                                         result=1))
        db_session.add(MatchPlayerRecord(match=match,
                                         player=player2,
                                         player_number=TicTacToeState.O_PLAYER,
                                         result=-1))
        player1, player2 = player2, player1
    return db_session


# noinspection DuplicatedCode
def test_load_history(memory_db):
    expected_summary = dedent("""\
        opponent levels [1 2 4 8]
        counts as 1 with 16 [1 0 0 0]
        wins as 1 with 16 [100   0   0   0]
        ties as 1 with 16 [0 0 0 0]
        counts as 2 with 16 [1 0 0 0]
        wins as 2 with 16 [0 0 0 0]
        ties as 2 with 16 [0 0 0 0]
        counts as 1 with 256 [0 0 0 0]
        wins as 1 with 256 [0 0 0 0]
        ties as 1 with 256 [0 0 0 0]
        counts as 2 with 256 [0 0 0 0]
        wins as 2 with 256 [0 0 0 0]
        ties as 2 with 256 [0 0 0 0]
        """)
    plot = StrengthPlot()
    plot.win_counter = WinCounter(player_levels=[16, 256],
                                  opponent_min=1,
                                  opponent_max=8)

    plot.load_history(memory_db)

    match_up: MatchUp = plot.win_counter[(16_000, False, 1_000, False)]
    assert match_up.p1_wins == 1
    assert plot.win_counter.build_summary() == expected_summary


# noinspection DuplicatedCode
def test_humans_excluded(memory_db):
    tic_tac_toe = memory_db.query(GameRecord).filter(
        GameRecord.name == 'Tic Tac Toe').one()
    player1 = memory_db.query(PlayerRecord).filter(
        PlayerRecord.milliseconds == 16_000).one()
    player2 = PlayerRecord(name='Mr. Human', type=PlayerRecord.HUMAN_TYPE)
    memory_db.add(player2)
    match = MatchRecord(game=tic_tac_toe)
    memory_db.add(match)
    memory_db.add(MatchPlayerRecord(match=match,
                                    player=player1,
                                    player_number=TicTacToeState.X_PLAYER,
                                    result=1))
    memory_db.add(MatchPlayerRecord(match=match,
                                    player=player2,
                                    player_number=TicTacToeState.O_PLAYER,
                                    result=-1))

    expected_summary = dedent("""\
        opponent levels [1 2 4 8]
        counts as 1 with 16 [1 0 0 0]
        wins as 1 with 16 [100   0   0   0]
        ties as 1 with 16 [0 0 0 0]
        counts as 2 with 16 [1 0 0 0]
        wins as 2 with 16 [0 0 0 0]
        ties as 2 with 16 [0 0 0 0]
        counts as 1 with 256 [0 0 0 0]
        wins as 1 with 256 [0 0 0 0]
        ties as 1 with 256 [0 0 0 0]
        counts as 2 with 256 [0 0 0 0]
        wins as 2 with 256 [0 0 0 0]
        ties as 2 with 256 [0 0 0 0]
        """)
    plot = StrengthPlot()
    plot.win_counter = WinCounter(player_levels=[16, 256],
                                  opponent_min=1,
                                  opponent_max=8)

    plot.load_history(memory_db)

    match_up: MatchUp = plot.win_counter[(16_000, False, 1_000, False)]
    assert match_up.p1_wins == 1
    assert plot.win_counter.build_summary() == expected_summary


# noinspection DuplicatedCode
def test_player_iterations_filtered(memory_db):
    tic_tac_toe = memory_db.query(GameRecord).filter(
        GameRecord.name == 'Tic Tac Toe').one()
    player1 = memory_db.query(PlayerRecord).filter(
        PlayerRecord.milliseconds == 16_000).one()
    player2 = PlayerRecord(name='Mr. Invincible',
                           type=PlayerRecord.PLAYOUT_TYPE,
                           milliseconds=100_000)
    memory_db.add(player2)
    match = MatchRecord(game=tic_tac_toe)
    memory_db.add(match)
    memory_db.add(MatchPlayerRecord(match=match,
                                    player=player1,
                                    player_number=TicTacToeState.X_PLAYER,
                                    result=1))
    memory_db.add(MatchPlayerRecord(match=match,
                                    player=player2,
                                    player_number=TicTacToeState.O_PLAYER,
                                    result=-1))

    expected_summary = dedent("""\
        opponent levels [1 2 4 8]
        counts as 1 with 16 [1 0 0 0]
        wins as 1 with 16 [100   0   0   0]
        ties as 1 with 16 [0 0 0 0]
        counts as 2 with 16 [1 0 0 0]
        wins as 2 with 16 [0 0 0 0]
        ties as 2 with 16 [0 0 0 0]
        counts as 1 with 256 [0 0 0 0]
        wins as 1 with 256 [0 0 0 0]
        ties as 1 with 256 [0 0 0 0]
        counts as 2 with 256 [0 0 0 0]
        wins as 2 with 256 [0 0 0 0]
        ties as 2 with 256 [0 0 0 0]
        """)
    plot = StrengthPlot()
    plot.win_counter = WinCounter(player_levels=[16, 256],
                                  opponent_min=1,
                                  opponent_max=8)

    plot.load_history(memory_db)

    match_up: MatchUp = plot.win_counter[(16_000, False, 1_000, False)]
    assert match_up.p1_wins == 1
    assert plot.win_counter.build_summary() == expected_summary


def test_plot_layout(pixmap_differ: PixmapDiffer, memory_db):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((500, 275)) as (actual, expected):
        fig = Figure()
        ax: Axes = fig.add_subplot(111)
        ax.set_title('Win Rates After 2 Games of Tic Tac Toe')
        ax.set_xlabel('Opponent MCTS simulation count')
        ax.set_ylabel('Win and tie rates')
        ax.set_ylim(-0.01, 1.01)
        ax.set_xscale('log')
        ax.plot([1, 2, 4, 8], [1, 0, 0, 0], 'C1', label='wins as 1 with 16')
        ax.plot([1, 2, 4, 8], [0, 0, 0, 0], 'C1:', label='ties as 1 with 16')
        ax.plot([1, 2, 4, 8], [0, 0, 0, 0], 'C1--', label='wins as 2 with 16')
        ax.plot([1, 2, 4, 8], [0, 0, 0, 0], 'C1-.', label='ties as 2 with 16')
        ax.plot([1, 2, 4, 8], [0, 0, 0, 0], 'C2', label='wins as 1 with 256')
        ax.plot([1, 2, 4, 8], [0, 0, 0, 0], 'C2:', label='ties as 1 with 256')
        ax.plot([1, 2, 4, 8], [0, 0, 0, 0], 'C2--', label='wins as 2 with 256')
        ax.plot([1, 2, 4, 8], [0, 0, 0, 0], 'C2-.', label='ties as 2 with 256')
        ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        fig.tight_layout()
        paint_figure(fig, expected)

        plot = StrengthPlot()
        plot.win_counter = WinCounter(player_levels=[16, 256],
                                      opponent_min=1,
                                      opponent_max=8)
        plot.load_history(memory_db)
        plot.create_plot()
        paint_figure(plot.axes.figure, actual)
