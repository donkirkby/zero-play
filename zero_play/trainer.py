import logging
from csv import DictWriter
from datetime import datetime
from itertools import count
from pathlib import Path

import pandas as pd

from zero_play.connect4.game import Connect4State
from zero_play.connect4.neural_net import NeuralNet
from zero_play.mcts_player import SearchManager, MctsPlayer

from zero_play.play_controller import PlayController
from zero_play.playout import Playout

logger = logging.getLogger(__name__)


def train(search_milliseconds: int,
          training_size: int,
          comparison_size: int,
          min_win_rate: float,
          data_folder: str):
    start_state = Connect4State()
    data_path = Path(data_folder)
    checkpoint_path = data_path / f'{start_state.game_name}-nn'
    checkpoint_path.mkdir(parents=True, exist_ok=True)
    history_path = data_path / f'{start_state.game_name}-history.csv'
    history_file = history_path.open('a')
    writer = DictWriter(history_file, ['wins_vs_base',
                                       'ties_vs_base',
                                       'wins_vs_best',
                                       'ties_vs_best',
                                       'date'])
    if not history_file.tell():
        writer.writeheader()
    best_net = NeuralNet(start_state)
    neural_net = NeuralNet(start_state)
    training_player = MctsPlayer(start_state, heuristic=neural_net)
    best_player = MctsPlayer(start_state, start_state.O_PLAYER, heuristic=best_net)
    base_player = MctsPlayer(start_state,
                             start_state.O_PLAYER,
                             milliseconds=search_milliseconds,
                             heuristic=Playout())

    best_file_name = 'best.h5'
    try:
        best_net.load_checkpoint(checkpoint_path, best_file_name)
    except OSError:
        best_net.save_checkpoint(checkpoint_path, best_file_name)

    base_controller = PlayController(start_state=start_state,
                                     players=[training_player, base_player])
    best_controller = PlayController(start_state=start_state,
                                     players=[training_player, best_player])
    search_manager = SearchManager(start_state, neural_net)
    for i in count():
        logger.info('Creating training data.')
        boards, outputs = search_manager.create_training_data(
            milliseconds=search_milliseconds,
            data_size=training_size)

        boards_path = data_path / 'boards.csv'
        outputs_path = data_path / 'outputs.csv'
        boards_df = pd.DataFrame(boards.reshape(training_size, 6*7))
        outputs_df = pd.DataFrame(outputs)
        boards_df.to_csv(boards_path)
        outputs_df.to_csv(outputs_path)

        filename = f'checkpoint-{i:02d}.h5'
        logger.info('Training for %s.', filename)
        neural_net.train(boards, outputs, './logs')

        logger.info('Testing.')
        wins_vs_base, base_ties, base_wins = base_controller.play(
            comparison_size,
            flip=True)
        wins_vs_best, best_ties, best_wins = best_controller.play(
            comparison_size,
            flip=True)
        writer.writerow(dict(wins_vs_base=wins_vs_base/comparison_size,
                             ties_vs_base=base_ties/comparison_size,
                             wins_vs_best=wins_vs_best/comparison_size,
                             ties_vs_best=best_ties/comparison_size,
                             date=datetime.now()))
        history_file.flush()
        win_rate_vs_base = calculate_win_rate(wins_vs_base, base_wins)
        win_rate_vs_best = calculate_win_rate(wins_vs_best, best_wins)
        if win_rate_vs_best < min_win_rate:
            decision = 'Rejected'
            neural_net.load_checkpoint(checkpoint_path, best_file_name)
        else:
            decision = 'Accepted'
            neural_net.save_checkpoint(checkpoint_path, filename)
            best_net.load_checkpoint(checkpoint_path, filename)
            best_net.save_checkpoint(checkpoint_path, best_file_name)
        logger.info('%s %s with wins %f over base (%d/%d/%d) and %f over best (%d/%d/%d).',
                    decision,
                    filename,
                    win_rate_vs_base,
                    wins_vs_base,
                    base_ties,
                    base_wins,
                    win_rate_vs_best,
                    wins_vs_best,
                    best_ties,
                    best_wins)
        search_manager.reset()


def calculate_win_rate(wins_vs_other, other_wins):
    total_wins = wins_vs_other + other_wins
    if total_wins:
        win_rate_vs_base = wins_vs_other / total_wins
        return win_rate_vs_base
    return 0.5
