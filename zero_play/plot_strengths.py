

# class Plotter:
#     def __init__(self,
#                  db_path,
#                  game_name: str,
#                  controller: typing.Optional[PlayController],
#                  player_definitions: typing.List[typing.Union[str, int]],
#                  opponent_min: int,
#                  opponent_max: int,
#                  neural_net_path: str):


def parse_args():
    parser = ArgumentParser(description='Plot player strengths.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('game',
                        default='zero_play.tictactoe.state.TicTacToeState',
                        nargs='?',
                        help='Game state class to test with.')
    parser.add_argument('--player_definitions',
                        nargs='*',
                        type=int,
                        help='list of definitions for player strength: number '
                             'of iterations, plus "nn" for neural net',
                        default=[8, 64, 512])
    parser.add_argument('--opponent_min',
                        help='minimum search iterations for the opponent',
                        type=int,
                        default=1)
    parser.add_argument('--opponent_max',
                        help='maximum search iterations for the opponent',
                        type=int,
                        default=512)
    parser.add_argument('--checkpoint',
                        help='checkpoint file to load for neural net')

    return parser.parse_args()


# def main():
#     logging.basicConfig(level=logging.INFO,
#                         format="%(asctime)s[%(levelname)s]:%(name)s:%(message)s")
#     logger.setLevel(logging.DEBUG)
#     args = parse_args()
#     class_path = args.game
#     class_parts = class_path.split('.')
#     class_name = class_parts.pop()
#     module_name = '.'.join(class_parts)
#     module = import_module(module_name)
#     game_state_class = getattr(module, class_name)
#     start_state: GameState = game_state_class()
#
#     # parser = args.parser
#     # parser.add_argument(
#     #     '-p', '--player',
#     #     default='mcts',
#     #     nargs='*',
#     #     help="the player to use",
#     #     action='entry_point')
#     # args.player = ['mcts']
#     # args.mcts_iterations = MctsPlayer.DEFAULT_MILLISECONDS
#
#     if '__live_coding_context__' in locals():
#         controller = None
#     else:
#         players = [MctsPlayer(start_state, GameState.X_PLAYER),
#                    MctsPlayer(start_state, GameState.O_PLAYER)]
#         controller = PlayController(start_state, players)
#
#     figure = plt.figure()
#     db_path = os.path.abspath(os.path.join(
#         __file__,
#         f'../../data/{args.game}-strengths.db'))
#     neural_net_path = os.path.abspath(os.path.join(
#         __file__,
#         f'../../data/{args.game}-nn/best.h5'))
#     logger.debug(db_path)
#     plotter = Plotter(db_path,
#                       args.game,
#                       controller,
#                       args.player_definitions,
#                       args.opponent_min,
#                       args.opponent_max,
#                       neural_net_path)
#     if controller is None:
#         animation = None
#     else:
#         animation = FuncAnimation(figure, plotter.update, interval=30000)
#
#     plt.show()
#     assert controller is None or animation is not None
#
#
# if __name__ in ('__main__', '__live_coding__'):
#     main()
