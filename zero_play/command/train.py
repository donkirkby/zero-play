import logging
from argparse import ArgumentDefaultsHelpFormatter, Namespace
from csv import DictWriter
from datetime import datetime
from itertools import count
from pathlib import Path

from zero_play.command.play import PlayController
from zero_play.connect4.neural_net import NeuralNet
from zero_play.mcts_player import SearchManager, MctsPlayer
from zero_play.command_parser import CommandParser
from zero_play.playout import Playout

logger = logging.getLogger(__name__)


def create_parser(subparsers):
    parser: CommandParser = subparsers.add_parser(
        'train',
        description='Train a neural network.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.set_defaults(handle=handle, parser=parser)
    parser.add_argument('game',
                        default='tictactoe',
                        help='the game to train for',
                        action='entry_point')
    parser.add_argument('--mcts_iterations',
                        type=int,
                        default=80,
                        help='the number of search iterations to generate '
                             'search data and compare models')
    parser.add_argument('--base_iterations',
                        type=int,
                        default=64,
                        help='the number of search iterations for the base player')
    parser.add_argument('--training_size',
                        type=int,
                        default=230,
                        help='the number of examples to generate')
    parser.add_argument('--comparison_games',
                        type=int,
                        default=40,
                        help='the number of games to compare two players')
    parser.add_argument('--min_win_rate',
                        type=float,
                        default=0.6,
                        help='minimum wins to replace previous model')


def handle(args: Namespace):
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s:%(name)s: %(message)s")
    parser = args.parser
    game = parser.load_argument(args, 'game')
    checkpoint_path = Path(f'data/{args.game}-nn')
    checkpoint_path.mkdir(parents=True, exist_ok=True)
    history_path = checkpoint_path.parent / f'{args.game}-history.csv'
    history_file = history_path.open('a')
    writer = DictWriter(history_file, ['wins_vs_base',
                                       'ties_vs_base',
                                       'wins_vs_best',
                                       'ties_vs_best',
                                       'date'])
    if not history_file.tell():
        writer.writeheader()
    best_net = NeuralNet(game)
    neural_net = NeuralNet(game)
    training_player = MctsPlayer(game, heuristic=[neural_net])
    best_player = MctsPlayer(game, game.O_PLAYER, heuristic=[best_net])
    base_player = MctsPlayer(game,
                             game.O_PLAYER,
                             mcts_iterations=[args.base_iterations],
                             heuristic=[Playout(game)])

    best_file_name = 'best.h5'
    try:
        best_net.load_checkpoint(checkpoint_path, best_file_name)
    except OSError:
        best_net.save_checkpoint(checkpoint_path, best_file_name)

    base_controller = PlayController(game=game,
                                     players=[training_player, base_player])
    best_controller = PlayController(game=game,
                                     players=[training_player, best_player])
    search_manager = SearchManager(game, neural_net)
    for i in count():
        logger.info('Creating training data.')
        boards, outputs = search_manager.create_training_data(
            args.mcts_iterations,
            data_size=args.training_size)

        filename = f'checkpoint-{i:02d}.h5'
        logger.info('Training for %s.', filename)
        neural_net.train(boards, outputs, './logs')

        logger.info('Testing.')
        wins_vs_base, base_ties, base_wins = base_controller.play(
            args.comparison_games,
            flip=True)
        wins_vs_best, best_ties, best_wins = best_controller.play(
            args.comparison_games,
            flip=True)
        writer.writerow(dict(wins_vs_base=wins_vs_base/args.comparison_games,
                             ties_vs_base=base_ties/args.comparison_games,
                             wins_vs_best=wins_vs_best/args.comparison_games,
                             ties_vs_best=best_ties/args.comparison_games,
                             date=datetime.now()))
        history_file.flush()
        win_rate_vs_base = calculate_win_rate(wins_vs_base, base_wins)
        win_rate_vs_best = calculate_win_rate(wins_vs_best, best_wins)
        if win_rate_vs_best < args.min_win_rate:
            decision = 'Rejected'
            neural_net.load_checkpoint(checkpoint_path, best_file_name)
        else:
            decision = 'Accepted'
            neural_net.save_checkpoint(checkpoint_path, filename)
            best_net.load_checkpoint(checkpoint_path, filename)
            best_net.save_checkpoint(checkpoint_path, best_file_name)
        logger.info('%s %s with wins %f over base and %f over best.',
                    decision,
                    filename,
                    win_rate_vs_base,
                    win_rate_vs_best)
        search_manager.reset()


def calculate_win_rate(wins_vs_other, other_wins):
    total_wins = wins_vs_other + other_wins
    if total_wins:
        win_rate_vs_base = wins_vs_other / total_wins
        return win_rate_vs_base
    return 0.5
