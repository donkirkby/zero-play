import itertools
import os
import typing
from csv import DictWriter
from io import StringIO

from zero_play.game import Game

import numpy as np


class LogDisplay:
    def __init__(self, game: Game):
        self.game = game
        self.step = 0
        self.file = StringIO()
        columns = ['event', 'step', 'player', 'move', 'comment']
        columns.extend(itertools.chain(*((f'choice{i}', f'prob{i}')
                                         for i in range(1, 11))))
        self.writer = DictWriter(self.file, columns, lineterminator=os.linesep)
        self.writer.writeheader()

    def record_move(self, board: np.ndarray, move: int, move_probabilities: typing.List[typing.Tuple[str, float]]):
        self.step += 1
        player = self.game.display_player(self.game.get_active_player(board))
        move_text = self.game.display_move(board, move)
        entry = dict(event='move',
                     step=self.step,
                     player=player,
                     move=move_text)
        for i, (choice, probability) in enumerate(move_probabilities, 1):
            entry[f'choice{i}'] = choice
            entry[f'prob{i}'] = probability
            if choice == move_text and i != 1:
                entry['comment'] = f'choice {i}'
        self.writer.writerow(entry)
