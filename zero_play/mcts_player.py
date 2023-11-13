import logging

import math
import typing
from concurrent.futures import (Future, wait, FIRST_COMPLETED, ALL_COMPLETED,
                                ProcessPoolExecutor)
from datetime import datetime
from itertools import count
from operator import itemgetter

import numpy as np

from zero_play.game_state import GameState
from zero_play.heuristic import Heuristic
from zero_play.player import Player

logger = logging.getLogger(__name__)


class SearchNode:
    # Controls exploration of new nodes vs. exploitation of good nodes.
    exploration_weight = 1.0

    def __init__(self,
                 game_state: GameState,
                 parent: typing.Optional['SearchNode'] = None,
                 move: int | None = None):
        """ Initialize an instance.

        :param game_state: the board state that this node represents
        :param parent: the board state that this node came from
        :param move: the move to get from parent to this node
        """
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children: typing.Optional[typing.List[SearchNode]] = None
        self.child_predictions: typing.Optional[np.ndarray] = None
        self.average_value = 0.0
        self.value_count = 0

    def __repr__(self):
        return f"SearchNode({self.game_state!r})"

    def __eq__(self, other):
        if isinstance(other, SearchNode):
            return self.game_state == other.game_state
        return NotImplemented

    def select_leaf(self):
        if self.value_count == 0:
            return self
        children = self.find_all_children()
        if not children:
            return self

        best_score = float('-inf')
        best_child = None
        for child in children:
            if self.child_predictions is None:
                prior = 1/len(children)
            else:
                prior = self.child_predictions[child.move]
            score = child.average_value + (self.exploration_weight * prior *
                                           math.sqrt(self.value_count) /
                                           (1 + child.value_count))
            if score > best_score:
                best_score = score
                best_child = child
        return best_child.select_leaf()

    def find_all_children(self) -> typing.List['SearchNode']:
        if self.children is not None:
            return self.children
        children: typing.List['SearchNode'] = []
        if self.game_state.is_ended():
            return children
        for move, is_valid in enumerate(self.game_state.get_valid_moves()):
            if is_valid:
                child_state = self.game_state.make_move(move)
                children.append(SearchNode(child_state, self, move))
        self.children = children
        return children

    def record_value(self,
                     value: float,
                     child_predictions: np.ndarray | None = None):
        if child_predictions is not None:
            self.child_predictions = child_predictions
        if (not self.parent or
                self.parent.game_state.get_active_player() !=
                self.game_state.get_active_player()):
            value *= -1
        self.average_value = ((self.average_value * self.value_count + value) /
                              (self.value_count + 1))
        self.value_count += 1
        if self.parent:
            self.parent.record_value(value)

    def evaluate(self, heuristic: Heuristic):
        value, child_predictions = heuristic.analyse(self.game_state)
        self.record_value(value, child_predictions)

    def choose_child(self, temperature: float) -> 'SearchNode':
        """ Choose a child randomly, ones with higher counts are more likely.

        :param temperature: positive value that controls how deterministic the
        choice is. The closer to zero, the more likely it is to choose the
        child with maximum count.
        """
        children = self.find_all_children()
        probabilities = self.rank_children(children, temperature)
        child_count = len(children)
        child_index = np.random.choice(child_count, p=probabilities)
        return children[child_index]

    @staticmethod
    def rank_children(children, temperature):
        values = np.array([temperature * child.value_count for child in children])

        # Avoid overflow by keeping the weights between 0 and 1.
        values -= values.max(initial=0)
        weights = np.exp(values)

        # Normalize the weights into probabilities that add up to 1.
        probabilities = weights / sum(weights)
        return probabilities

    def find_best_children(self):
        children = self.find_all_children()
        best_value = float('-inf')
        best_children = []
        for child in children:
            child_value = child.average_value
            if child_value > best_value:
                best_children = [child]
                best_value = child_value
            elif child_value == best_value:
                best_children.append(child)
        return best_children


class SearchManager:
    def __init__(self, start_state: GameState,
                 heuristic: Heuristic,
                 process_count: int = 1):
        self.start_state = start_state
        self.heuristic = heuristic
        self.current_node = self.reset()
        self.process_count = process_count
        if process_count <= 1:
            self.executor = None
        else:
            self.executor = ProcessPoolExecutor(process_count)
        self.tasks: typing.Dict[Future, SearchNode] = {}
        self.search_count = 0
        self.total_iterations = 0
        self.total_milliseconds = 0

    @property
    def average_iterations(self) -> float:
        if self.search_count == 0:
            return math.nan
        return self.total_iterations / self.search_count

    @property
    def average_milliseconds(self) -> float:
        if self.search_count == 0:
            return math.nan
        return self.total_milliseconds / self.search_count

    def reset_counts(self) -> None:
        self.search_count = self.total_milliseconds = self.total_iterations = 0

    def reset(self) -> SearchNode:
        self.current_node = SearchNode(self.start_state)
        return self.current_node

    def find_node(self, game_state: GameState):
        if not game_state == self.current_node.game_state:
            for child in self.current_node.find_all_children():
                if game_state == child.game_state:
                    self.current_node = child
                    break
            else:
                parent = self.current_node.parent
                if parent is not None and game_state == parent.game_state:
                    self.current_node = parent
                else:
                    self.current_node = SearchNode(game_state)

    def search(self,
               board: GameState,
               iterations: int | None = 1,
               milliseconds: int | None = None):
        start_time = datetime.now()
        self.find_node(board)
        max_tasks = self.process_count * 2
        iteration = 0
        for iteration in count(1):
            leaf = self.current_node.select_leaf()
            if self.executor is None:
                leaf.evaluate(self.heuristic)
            else:
                future = self.executor.submit(self.heuristic.analyse,
                                              leaf.game_state)
                self.tasks[future] = leaf
                if len(self.tasks) >= max_tasks:
                    timeout = None
                else:
                    timeout = 0
                self.check_tasks(timeout, return_when=FIRST_COMPLETED)
            if iterations is not None:
                if iteration >= iterations:
                    break
            else:
                assert milliseconds is not None
                spent_seconds = (datetime.now() - start_time).total_seconds()
                if spent_seconds*1000 > milliseconds:
                    break
        if self.tasks:
            self.check_tasks(timeout=None, return_when=ALL_COMPLETED)

        if self.current_node.children is None:
            self.current_node.select_leaf()
        self.search_count += 1
        self.total_iterations += iteration
        spent_ms = (datetime.now() - start_time).total_seconds() * 1000
        self.total_milliseconds += round(spent_ms)

    def check_tasks(self, timeout, return_when):
        done, not_done = wait(self.tasks.keys(),
                              timeout,
                              return_when=return_when)
        for done_future in done:
            done_leaf = self.tasks.pop(done_future)
            value, child_predictions = done_future.result()
            done_leaf.record_value(value, child_predictions)

    def get_best_move(self) -> int:
        best_children = self.current_node.find_best_children()
        # noinspection PyTypeChecker
        self.current_node = child = np.random.choice(best_children)
        assert child.move is not None
        return child.move

    def choose_weighted_move(self) -> int:
        temperature = 1.0
        self.current_node = child = self.current_node.choose_child(temperature)
        assert child.move is not None
        return child.move

    def get_move_probabilities(
            self,
            game_state: GameState,
            limit: int = 10) -> typing.List[typing.Tuple[str,
                                                         float,
                                                         int,
                                                         float]]:
        """ Report the probability that each move is the best choice.

        :param game_state: the starting position
        :param limit: the maximum number of moves to report
        :return: [(move_display, probability, value_count, avg_value)], where
        value_count is the number of times the value was probed from the move,
        and avg_value is the average value from all those probes.
        """
        self.find_node(game_state)
        children = self.current_node.find_all_children()
        temperature = 1.0
        probabilities = self.current_node.rank_children(children, temperature)
        value_counts = [child.value_count for child in children]
        ranked_children = sorted(zip(value_counts, probabilities, children),
                                 key=itemgetter(0),
                                 reverse=True)
        top_children = ranked_children[:limit]
        child_node: SearchNode
        top_moves = [(game_state.display_move(child_node.move),
                      probability,
                      value_count,
                      child_node.average_value)
                     for value_count, probability, child_node in top_children
                     if child_node.move is not None]
        return top_moves

    def create_training_data(
            self,
            iterations: int | None = None,
            milliseconds: int | None = None,
            data_size: int = 1) -> typing.Tuple[np.ndarray, np.ndarray]:
        """ Play several games, then return game states and analysis.

        Specify iterations or milliseconds to control the amount of search.

        :param iterations: number of search iterations to run on each game state
        :param milliseconds: time to search on each game state
        :param data_size: number of game states to return
        :return: (game_states, outputs) - both are numpy arrays. Each item in
        game_states is a single game state, corresponding to an item at the same
        index in outputs. Each item in outputs is a list of moves, with the
        normalized weights for choosing each move, plus an extra entry that is
        the final value of this position for the active player.
        """
        game_states: typing.List[typing.Tuple[GameState, np.ndarray]] = []
        self.search(self.current_node.game_state, iterations=1)  # One extra to start.
        report_size = 0
        board_shape = self.current_node.game_state.spaces.shape
        boards = np.zeros((data_size,) + board_shape, np.uint8)
        move_count = self.current_node.game_state.get_valid_moves().size
        outputs = np.zeros((data_size, move_count + 1))
        data_count = 0
        while True:
            self.search(self.current_node.game_state,
                        iterations=iterations,
                        milliseconds=milliseconds)
            assert self.current_node.children is not None
            assert self.current_node.child_predictions is not None
            move_weights = np.zeros(self.current_node.child_predictions.size)
            for child in self.current_node.children:
                move = child.move
                move_weights[move] = child.value_count
            total_weight = move_weights.sum()
            if total_weight:
                move_weights /= total_weight
            game_states.append((self.current_node.game_state, move_weights))
            move = np.random.choice(move_weights.size, p=move_weights)
            for child in self.current_node.children:
                if child.move == move:
                    self.current_node = child
                    break
            if self.current_node.game_state.is_ended():
                final_value, _ = self.heuristic.analyse(self.current_node.game_state)
                final_player = -self.current_node.game_state.get_active_player()
                for game_state, move_weights in game_states:
                    value = final_value
                    if game_state.get_active_player() != final_player:
                        value *= -1
                    boards[data_count] = game_state.get_spaces()
                    outputs[data_count, :move_count] = move_weights
                    outputs[data_count, -1] = value
                    data_count += 1
                    if data_count >= data_size:
                        return boards, outputs

                if data_count > report_size:
                    logger.debug('Created %d training examples so far.', data_count)
                    report_size = data_count * 2
                game_states.clear()
                self.reset()

                # One extra to start the next game.
                self.search(self.current_node.game_state, iterations=1)


class MctsPlayer(Player):
    """ Use Monte Carlo Tree Search to choose moves in a game.

    This is based on the general discussion of MCTS in Wikipedia:
    https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    Also based on the specific adaptations of AlphaZero:
    https://web.stanford.edu/~surag/posts/alphazero.html
    The original AlphaZero paper:
    https://deepmind.com/blog/alphago-zero-learning-scratch/
    """
    DEFAULT_ITERATIONS = 80

    def __init__(self,
                 start_state: GameState,
                 player_number: int = GameState.X_PLAYER,
                 iteration_count: int | None = None,
                 milliseconds: int | None = None,
                 heuristic: Heuristic | None = None,
                 process_count: int = 1):
        super().__init__(player_number, heuristic)
        self.milliseconds = milliseconds
        if milliseconds is None and iteration_count is None:
            self.iteration_count: int | None = self.DEFAULT_ITERATIONS
        else:
            self.iteration_count = iteration_count
        self.search_manager = SearchManager(start_state,
                                            self.heuristic,
                                            process_count)

    @property
    def heuristic(self) -> Heuristic:
        return self._heuristic

    @heuristic.setter
    def heuristic(self, value: Heuristic):
        self._heuristic = value
        search_manager = getattr(self, 'search_manager', None)
        if search_manager is not None:
            search_manager.heuristic = value

    def reset_counts(self) -> None:
        self.search_manager.reset_counts()

    @property
    def average_iterations(self) -> float:
        return self.search_manager.average_iterations

    @property
    def average_milliseconds(self) -> float:
        return self.search_manager.average_milliseconds

    def end_game(self, game_state: GameState, opponent: Player):
        self.search_manager.reset()

    def choose_move(self, game_state: GameState) -> int:
        """ Choose a move for the given board.

        :param game_state: the current state of the game.
        :return: the chosen move's index in the list of valid moves.
        """
        self.search_manager.search(game_state,
                                   self.iteration_count,
                                   self.milliseconds)
        if game_state.get_move_count() < 15:
            return self.search_manager.choose_weighted_move()
        return self.search_manager.get_best_move()

    def get_move_probabilities(self, game_state: GameState) -> typing.List[
            typing.Tuple[str, float, int, float]]:
        """ Report the probability that each move is the best choice.

        :param game_state: the board to analyse
        :return: [(move_display, probability, value_count, avg_value)], where
        value_count is the number of times the value was probed from the move,
        and avg_value is the average value from all those probes.
        """
        return self.search_manager.get_move_probabilities(game_state)

    def get_summary(self) -> typing.Sequence[str]:
        if self.milliseconds is not None:
            return (('mcts',) + tuple(self.heuristic.get_summary()) +
                    (f'{self.milliseconds}ms search',))
        return (('mcts',) + tuple(self.heuristic.get_summary()) +
                (f'{self.iteration_count} iterations',))
