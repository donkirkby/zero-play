import itertools
import os
import typing
from csv import DictWriter
from dataclasses import dataclass
from io import StringIO

from zero_play.game import Game

import numpy as np


@dataclass
class LogItem:
    step: int
    player: str
    move_text: str
    board: np.ndarray
    comment: str = ''
    choices: typing.Sequence[typing.Tuple[str, float]] = ()

    def __str__(self):
        suffix = f' ({self.comment})' if self.comment else ''
        return f'{self.step}: {self.player} - {self.move_text}{suffix}'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.step == other.step and
                self.player == other.player and
                self.move_text == other.move_text and
                np.array_equal(self.board, other.board) and
                self.comment == other.comment and
                self.choices == other.choices)


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
        self.items: typing.List[LogItem] = []
        self.offsets: typing.List[int] = []

    def record_move(self, board: np.ndarray, move: int):
        self.step += 1
        player = self.game.display_player(self.game.get_active_player(board))
        move_text = self.game.display_move(board, move)
        self.items.append(LogItem(self.step, player, move_text, board))

    def analyse_move(self,
                     board: np.ndarray,
                     analysing_player: int,
                     move_probabilities: typing.List[typing.Tuple[str, float]]):
        for item in reversed(self.items):
            if np.array_equal(item.board, board):
                break
        else:
            raise ValueError('Board not found in log.')
        active_player = self.game.get_active_player(board)
        if item.choices and active_player != analysing_player:
            return
        item.choices = move_probabilities
        for i, (choice, probability) in enumerate(move_probabilities, 1):
            if choice == item.move_text and i != 1:
                item.comment = f'choice {i}'
