import logging
import os
import sqlite3
import typing
from argparse import ArgumentDefaultsHelpFormatter
from multiprocessing import Process, Queue
from queue import Empty
from sqlite3 import OperationalError

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sn

from zero_play.command.play import PlayController
from zero_play.game import Game
from zero_play.mcts_player import MctsPlayer
from zero_play.zero_play import CommandParser

logger = logging.getLogger(__name__)


class Plotter:
    def __init__(self,
                 db_path,
                 game_name: str,
                 controller: PlayController = None):
        self.x = 2 << np.arange(7)
        self.y = 2 << np.arange(7)
        self.x_coords, self.y_coords = np.meshgrid(self.x, self.y)
        self.counts = np.zeros(self.y_coords.shape)
        self.y_wins = np.zeros(self.y_coords.shape)
        self.result_queue: Queue = Queue()
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.load_history()
        self.has_reported = False
        self.game_name = game_name
        if controller is not None:
            game_thread = Process(target=run_games,
                                  args=(controller,
                                        self.result_queue,
                                        self.x,
                                        self.y,
                                        self.counts.copy()),
                                  daemon=True)
            game_thread.start()
        sn.set()
        plt.ylabel('Player 1 MCTS simulation count')
        plt.xlabel('Player 2 MCTS simulation count')
        plt.xscale('log')
        plt.yscale('log')
        self.artists: typing.List[plt.Artist] = []
        self.contour = None
        self.colorbar_axes = None
        self.create_contour()
        plt.tight_layout()

    def update(self, _frame):
        messages = []
        try:
            for _ in range(1000):
                messages.append(self.result_queue.get_nowait())
        except Empty:
            pass
        logger.debug('Plotter.update() found %d messages.', len(messages))
        if not messages:
            return
        for x, y, result in messages:
            if result < -0.1:
                wins1 = 0
            elif result > 0.1:
                wins1 = 1
            else:
                wins1 = 0.5
            self.record_result(y, x, wins1)
        self.write_history()

        for artist in self.contour.collections:
            artist.remove()
        self.artists.clear()

        self.create_contour()
        logger.debug('Plotter.update() done.')
        return self.artists

    def record_result(self, strength1, strength2, wins1, count=1):
        matches = np.nonzero(self.y == strength1)
        if not matches:
            return
        i = matches[0]
        matches = np.nonzero(self.x == strength2)
        if not matches:
            return
        j = matches[0]
        self.y_wins[i, j] += wins1
        self.counts[i, j] += count

    def create_contour(self):
        safe_counts = self.counts + (self.counts == 0)  # Avoid dividing by 0.
        z = self.y_wins / safe_counts
        if not self.has_reported:
            # print(self.y_wins)
            print(self.counts)
            print(z)
            self.has_reported = True
        # np.savetxt(sys.stdout, z)
        self.contour = plt.contourf(self.x_coords, self.y_coords, z)
        self.artists.append(self.contour)
        # self.artists.append(plt.clabel(self.contour))
        self.artists.append(plt.title(
            f'Player 1 Win Rates After {int(self.counts.sum())} '
            f'Games of {self.game_name}'))
        colorbar = plt.colorbar(cax=self.colorbar_axes)
        self.artists.append(colorbar)
        _, self.colorbar_axes = plt.gcf().get_axes()

    def load_history(self):
        try:
            self.conn.execute("""\
CREATE
TABLE   games
        (
        strength1,
        strength2,
        count,
        wins1
        );
""")
        except OperationalError:
            # Table already exists.
            pass
        cursor = self.conn.execute("""\
SELECT  strength1,
        strength2,
        wins1,
        count
FROM    games;""")
        while True:
            rows = cursor.fetchmany()
            if not rows:
                break
            for row in rows:
                self.record_result(*row)

    def write_history(self):
        it = np.nditer(self.counts, flags=['multi_index'])
        while not it.finished:
            i, j = it.multi_index
            strength1 = int(self.y[i])
            strength2 = int(self.x[j])
            wins1 = int(self.y_wins[i, j])
            count = int(it[0])
            update_count = self.conn.execute(
                """\
UPDATE  games
SET     wins1 = ?,
        count = ?
WHERE   strength1 = ?
AND     strength2 = ?;
""",
                [wins1, count, strength1, strength2]).rowcount
            if update_count == 0:
                self.conn.execute(
                    """\
INSERT
INTO    games
        (
        strength1,
        strength2,
        count,
        wins1
        )
        VALUES
        (
        ?,
        ?,
        ?,
        ?
        )
""",
                    [strength1, strength2, count, wins1])
            self.conn.commit()
            it.iternext()


def run_games(controller: PlayController, result_queue: Queue, x_values, y_values, counts):
    player1: MctsPlayer = controller.players[Game.X_PLAYER]
    player2: MctsPlayer = controller.players[Game.O_PLAYER]
    game_count = 0

    while True:
        for j, x in enumerate(x_values):
            player2.iteration_count = x
            for i, y in enumerate(y_values):
                player1.iteration_count = y
                # logger.debug(f'checking params {i}, {j} ({x}, {y}) with {counts[i, j]} counts')
                if counts[i, j] > counts.min():
                    continue
                counts[i, j] += 1
                controller.start_game()
                while not controller.take_turn():
                    pass

                result = controller.game.get_winner(controller.board)

                logger.debug(f'Result of pitting {y} vs {x}: {result}.')
                result_queue.put((x, y, result))
                # if game_count % 100 == 0:
                #     start_time = datetime.now()
                #     plt.pause(0.0001)
                #     update_duration = datetime.now() - start_time
                #     logger.debug('Updated plot in %s.', update_duration)
                game_count += 1


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s[%(levelname)s]:%(name)s:%(message)s")
    logger.setLevel(logging.DEBUG)
    parser = CommandParser(description='Plot player strengths.',
                           formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('game',
                        default='tictactoe',
                        help='the game to play',
                        action='entry_point')

    args = parser.parse_args()
    parser.add_argument(
        '-p', '--player',
        default='mcts',
        nargs='*',
        help="the player to use",
        action='entry_point')
    args.player = ['mcts']
    args.mcts_iterations = MctsPlayer.DEFAULT_ITERATIONS

    if __name__ == '__live_coding__':
        controller = None
    else:
        controller = PlayController(parser, args)

    figure = plt.figure()
    db_path = os.path.abspath(os.path.join(
        __file__,
        f'../../../data/{args.game}-strengths.db'))
    logger.debug(db_path)
    plotter = Plotter(db_path, args.game, controller)
    # noinspection PyUnusedLocal
    animation = FuncAnimation(figure, plotter.update, interval=30000)
    plt.show()


if __name__ == '__main__':
    main()
