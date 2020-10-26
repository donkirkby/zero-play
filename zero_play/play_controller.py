import typing
from datetime import datetime

from zero_play.game_state import GameState
from zero_play.player import Player


class PlayerResults:
    def __init__(self, player: Player):
        self.player = player
        self.total_time = 0.0
        self.move_count = self.win_count = 0
        self.summary = player.get_summary()

    def get_summary(self):
        if self.move_count:
            move_time = self.total_time / self.move_count
        else:
            move_time = 0.0
        return f'{self.summary} - {self.win_count} wins, {move_time:0.3}s/move'


class PlayController:
    def __init__(self, start_state: GameState, players: typing.List[Player]):
        self.board = self.start_state = start_state
        x_player: Player
        o_player: Player
        x_player, o_player = players
        x_player.player_number = start_state.X_PLAYER
        o_player.player_number = start_state.O_PLAYER
        self.players = {start_state.X_PLAYER: x_player,
                        start_state.O_PLAYER: o_player}
        self.results = [PlayerResults(x_player), PlayerResults(o_player)]
        self.start_game()

    def start_game(self):
        self.board = self.start_state

    def take_turn(self) -> bool:
        """ Take one turn in the game, and return True if the game is over. """
        player_number = self.board.get_active_player()
        player = self.players[player_number]
        start_time = datetime.now()
        move = player.choose_move(self.board)
        move_duration = datetime.now() - start_time
        player_results = self.get_player_results(player)
        player_results.total_time += move_duration.total_seconds()
        player_results.move_count += 1
        self.board = self.board.make_move(move)
        if not self.board.is_ended():
            return False

        other_player = self.players[-player_number]
        player.end_game(self.board, other_player)
        other_player.end_game(self.board, player)

        return True

    def get_player_results(self, player: Player) -> PlayerResults:
        for player_results in self.results:
            if player_results.player is player:
                return player_results
        raise ValueError('Player not found.')

    def play(self, games: int = 1, flip: bool = False, display: bool = False):
        current_x = original_x = self.players[self.start_state.X_PLAYER]
        current_o = original_o = self.players[self.start_state.O_PLAYER]
        self.results = [PlayerResults(current_x), PlayerResults(current_o)]
        ties = 0
        for i in range(games):
            if i and flip:
                current_x = self.players[self.start_state.O_PLAYER]
                current_o = self.players[self.start_state.X_PLAYER]
                current_x.player_number = self.start_state.X_PLAYER
                current_o.player_number = self.start_state.O_PLAYER
                self.players[self.start_state.X_PLAYER] = current_x
                self.players[self.start_state.O_PLAYER] = current_o
            while True:
                if display:
                    print(self.board.display(show_coordinates=True))
                if self.take_turn():
                    break
            if display:
                print(self.board.display(show_coordinates=True))
            if self.board.is_win(self.board.X_PLAYER):
                self.get_player_results(current_x).win_count += 1
            elif self.board.is_win(self.board.O_PLAYER):
                self.get_player_results(current_o).win_count += 1
            else:
                ties += 1
            self.start_game()
        original_x.player_number = self.board.X_PLAYER
        original_o.player_number = self.board.O_PLAYER
        self.players[self.board.X_PLAYER] = original_x
        self.players[self.board.O_PLAYER] = original_o
        for player_results in self.results:
            print(player_results.get_summary())
        print(ties, 'ties')
        x_results = self.get_player_results(original_x)
        o_results = self.get_player_results(original_o)

        return x_results.win_count, ties, o_results.win_count
