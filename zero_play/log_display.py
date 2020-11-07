import typing
from dataclasses import dataclass

from zero_play.game_state import GameState


@dataclass
class LogItem:
    step: int
    player: str
    move_text: str
    game_state: GameState
    comment: str = ''

    # [(move_display, probability, value_count, avg_value)]
    choices: typing.Sequence[typing.Tuple[str, float, int, float]] = ()

    def __str__(self):
        suffix = f' ({self.comment})' if self.comment else ''
        return f'{self.step}: {self.player} - {self.move_text}{suffix}'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.step == other.step and
                self.player == other.player and
                self.move_text == other.move_text and
                self.game_state == other.game_state and
                self.comment == other.comment and
                self.choices == other.choices)


class LogDisplay:
    def __init__(self):
        self.step = 0
        self.items: typing.List[LogItem] = []
        self.offsets: typing.List[int] = []

    def record_move(self, game_state: GameState, move: int):
        self.step += 1
        player = game_state.display_player(game_state.get_active_player())
        move_text = game_state.display_move(move)
        self.items.append(LogItem(self.step, player, move_text, game_state))

    def analyse_move(
            self,
            game_state: GameState,
            analysing_player: int,
            move_probabilities: typing.List[typing.Tuple[str,
                                                         float,
                                                         int,
                                                         float]]):
        """ Record analysis of the choices for a move.

        :param game_state: the state before the move
        :param analysing_player: the player doing the analysis; if both players
            report analysis, the active player's will be kept
        :param move_probabilities: the detailed analysis of best valid moves
            [(choice, probability, count, value)] where choice is the move
            display, probability is the recommended probability of choosing that
            move, count is the number of times the move or a descendant was
            analysed during the search, and value is the estimated value of the
            move, where 1 is 100% wins for the active player and -1 is 100%
            losses.
        """
        for item in reversed(self.items):
            if item.game_state == game_state:
                break
        else:
            raise ValueError('Board not found in log.')
        active_player = game_state.get_active_player()
        if item.choices and active_player != analysing_player:
            return
        item.choices = move_probabilities
        for i, (choice,
                probability,
                count,
                value) in enumerate(move_probabilities, 1):
            if choice == item.move_text:
                if i != 1:
                    item.comment = f'choice {i}'
                break
        else:
            # Didn't find chosen move in analysed moves, probably a poor choice.
            item.comment = '?'

    def rewind_to(self, step: int):
        del self.items[step:]
        self.step = step
