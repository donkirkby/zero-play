import typing
from argparse import Namespace, ArgumentDefaultsHelpFormatter

import numpy as np

from zero_play.game import Game
from zero_play.command_parser import CommandParser
from zero_play.player import Player, get_player_argument


class PlayController:
    def __init__(self, args: Namespace = None, game: Game = None, players: typing.List[Player] = None):
        if args is None:
            assert game is not None
            assert players is not None
            self.game = game
            x_player, o_player = players
            x_player.player_number = game.X_PLAYER
            o_player.player_number = game.O_PLAYER
            self.players = {Game.X_PLAYER: x_player, Game.O_PLAYER: o_player}
        else:
            parser: CommandParser = args.parser
            self.game: Game = parser.load_argument(args, 'game')
            player_names = args.player
            self.players = {
                Game.X_PLAYER: parser.load_argument(
                    args,
                    'player',
                    get_player_argument(player_names, Game.X_PLAYER),
                    game=self.game,
                    player_number=Game.X_PLAYER),
                Game.O_PLAYER: parser.load_argument(
                    args,
                    'player',
                    get_player_argument(player_names, Game.O_PLAYER),
                    game=self.game,
                    player_number=Game.O_PLAYER)}
        self.board: np.ndarray = None
        self.start_game()

    def start_game(self):
        self.board = self.game.create_board()

    def take_turn(self) -> bool:
        """ Take one turn in the game, and return True if the game is over. """
        player_number = self.game.get_active_player(self.board)
        player = self.players[player_number]
        move = player.choose_move(self.board)
        self.board = self.game.make_move(self.board, move)
        if not self.game.is_ended(self.board):
            return False

        other_player = self.players[-player_number]
        player.end_game(self.board, other_player)
        other_player.end_game(self.board, player)

        return True

    def play(self, games: int = 1, flip: bool = False):
        current_x = original_x = self.players[self.game.X_PLAYER]
        current_o = original_o = self.players[self.game.O_PLAYER]
        wins = {original_x: 0,
                original_o: 0}
        ties = 0
        for i in range(games):
            if i and flip:
                current_x = self.players[self.game.O_PLAYER]
                current_o = self.players[self.game.X_PLAYER]
                current_x.player_number = self.game.X_PLAYER
                current_o.player_number = self.game.O_PLAYER
                self.players[self.game.X_PLAYER] = current_x
                self.players[self.game.O_PLAYER] = current_o
            while not self.take_turn():
                pass
            if self.game.is_win(self.board, self.game.X_PLAYER):
                wins[current_x] += 1
            elif self.game.is_win(self.board, self.game.O_PLAYER):
                wins[current_o] += 1
            else:
                ties += 1
            self.start_game()
        original_x.player_number = self.game.X_PLAYER
        original_o.player_number = self.game.O_PLAYER
        self.players[self.game.X_PLAYER] = original_x
        self.players[self.game.O_PLAYER] = original_o

        return wins[original_x], ties, wins[original_o]


def create_parser(subparsers):
    parser: CommandParser = subparsers.add_parser(
        'play',
        description='Pit two players against each other.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.set_defaults(handle=handle, parser=parser)
    parser.add_argument('game',
                        default='tictactoe',
                        help='the game to play',
                        action='entry_point')
    parser.add_argument(
        '-p', '--players',
        default=['human', 'mcts'],
        nargs='*',
        help="the player to use, pass two names if they're different",
        action='entry_point',
        dest='player')
    parser.add_argument('--heuristic',
                        default=['playout'],
                        nargs='*',
                        help='heuristic for evaluating boards',
                        action='entry_point')


def handle(args: Namespace):
    controller = PlayController(args)
    controller.play()
