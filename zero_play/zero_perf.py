from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from importlib import import_module

from zero_play.game_state import GameState
from zero_play.mcts_player import MctsPlayer
from zero_play.play_controller import PlayController


def parse_args():
    # noinspection PyTypeChecker
    parser = ArgumentParser(description='Run a game scenario with Zero Play, '
                                        'and report the slowest code.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('game',
                        default='zero_play.tictactoe.state.TicTacToeState',
                        nargs='?',
                        help='Game state class to test with.')
    parser.add_argument('game_count',
                        type=int,
                        default=1,
                        nargs='?',
                        help='Limit the number of games to run.')
    parser.add_argument('--flip',
                        action='store_true',
                        help='Flip first player after every game.')
    parser.add_argument('--iter1',
                        type=int,
                        default=100,
                        help='Number of search iterations for player 1.')
    parser.add_argument('--iter2',
                        type=int,
                        default=100,
                        help='Number of search iterations for player 2.')
    parser.add_argument('--processes1',
                        type=int,
                        default=1,
                        help='Number of parallel search processes for player 1.')
    parser.add_argument('--processes2',
                        type=int,
                        default=1,
                        help='Number of parallel search processes for player 2.')
    parser.add_argument('--display',
                        action='store_true',
                        help='Display moves in the games.')
    return parser.parse_args()


def main():
    args = parse_args()
    class_path = args.game
    class_parts = class_path.split('.')
    class_name = class_parts.pop()
    module_name = '.'.join(class_parts)
    module = import_module(module_name)
    game_state_class = getattr(module, class_name)
    start_state: GameState = game_state_class()

    player1 = MctsPlayer(start_state,
                         iteration_count=args.iter1,
                         process_count=args.processes1)
    player2 = MctsPlayer(start_state,
                         iteration_count=args.iter2,
                         process_count=args.processes2)
    controller = PlayController(start_state, [player1, player2])
    controller.play(args.game_count, args.flip, args.display)


if __name__ == '__main__':
    main()
