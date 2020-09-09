import logging

import math
import typing
from operator import itemgetter

import numpy as np

from zero_play.game import Game
from zero_play.heuristic import Heuristic
from zero_play.player import Player

logger = logging.getLogger(__name__)


class SearchNode:
    # Controls exploration of new nodes vs. exploitation of good nodes.
    exploration_weight = 1.0

    def __init__(self, game: Game,
                 board: np.ndarray = None,
                 parent: 'SearchNode' = None,
                 move: int = None):
        """ Initialize an instance.

        :param board: the board state that this node represents
        :param parent: the board state that this node came from
        :param move: the move to get from parent to this node
        """
        self.game = game
        if board is None:
            self.board = game.create_board()
        else:
            self.board = board
        self.parent = parent
        self.move = move
        self.children: typing.Optional[typing.List[SearchNode]] = None
        self.child_predictions: typing.Optional[np.ndarray] = None
        self.average_value = 0.0
        self.value_count = 0

    def __repr__(self):
        board_repr = " ".join(repr(self.board).split())
        board_repr = board_repr.replace('[ ', '[')
        return f"SearchNode({self.game!r}, {board_repr})"

    def __eq__(self, other):
        if isinstance(other, SearchNode):
            return np.array_equal(self.board, other.board)
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
        children = []
        for move, is_valid in enumerate(self.game.get_valid_moves(self.board)):
            if is_valid:
                child_board = self.game.make_move(self.board, move)
                children.append(SearchNode(self.game,
                                           child_board,
                                           self,
                                           move))
        self.children = children
        return children

    def record_value(self, value):
        self.average_value = ((self.average_value * self.value_count + value) /
                              (self.value_count + 1))
        self.value_count += 1
        if self.parent:
            self.parent.record_value(-value)

    def evaluate(self, heuristic: Heuristic):
        value, child_predictions = heuristic.analyse(self.board)
        self.child_predictions = child_predictions
        self.record_value(value)

    def choose_child(self, temperature: float) -> 'SearchNode':
        """ Choose a child randomly, ones with higher counts are more likely.

        :param temperature: positive value that controls how deterministic the
        choice is. The closer to zero, the more likely it is to choose the
        child with maximum count.
        """
        children = self.find_all_children()
        probabilities = self.rank_children(children, temperature)
        child = np.random.choice(children, p=probabilities)
        return child

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
    def __init__(self, game: Game, heuristic: Heuristic):
        self.game = game
        self.heuristic = heuristic
        self.current_node = self.reset()

    def reset(self) -> SearchNode:
        self.current_node = SearchNode(self.game)
        return self.current_node

    def find_node(self, board):
        if not np.array_equal(board, self.current_node.board):
            for child in self.current_node.find_all_children():
                if np.array_equal(board, child.board):
                    self.current_node = child
                    break
            else:
                parent = self.current_node.parent
                if parent is not None and np.array_equal(parent.board, board):
                    self.current_node = parent
                else:
                    self.current_node = SearchNode(self.game, board)

    def search(self, board: np.ndarray, iterations: int):
        self.find_node(board)
        for _ in range(iterations):
            leaf = self.current_node.select_leaf()
            leaf.evaluate(self.heuristic)
        if self.current_node.children is None:
            self.current_node.select_leaf()

    def get_best_move(self) -> int:
        best_children = self.current_node.find_best_children()
        self.current_node = np.random.choice(best_children)
        assert self.current_node.move is not None
        return self.current_node.move

    def choose_weighted_move(self) -> int:
        temperature = 1.0
        child = self.current_node.choose_child(temperature)
        assert child.move is not None
        return child.move

    def get_move_probabilities(
            self,
            board: np.ndarray,
            limit: int = 10) -> typing.List[typing.Tuple[str,
                                                         float,
                                                         int,
                                                         float]]:
        """ Report the probability that each move is the best choice.

        :param board: the starting position
        :param limit: the maximum number of moves to report
        :return: [(move_display, probability, value_count, avg_value)], where
        value_count is the number of times the value was probed from the move,
        and avg_value is the average value from all those probes.
        """
        self.find_node(board)
        children = self.current_node.find_all_children()
        temperature = 1.0
        probabilities = self.current_node.rank_children(children, temperature)
        ranked_children = sorted(zip(probabilities, children),
                                 key=itemgetter(0),
                                 reverse=True)
        top_children = ranked_children[:limit]
        child_node: SearchNode
        top_moves = [(self.game.display_move(board, child_node.move),
                      probability,
                      child_node.value_count,
                      child_node.average_value)
                     for probability, child_node in top_children
                     if child_node.move is not None]
        return top_moves

    def create_training_data(self, iterations: int, data_size: int):
        game_states = []
        self.search(self.current_node.board, iterations=1)  # One extra to start.
        report_size = 0
        board_shape = self.game.get_spaces(self.current_node.board).shape
        boards = np.zeros((data_size,) + board_shape, int)
        move_count = self.game.get_valid_moves(self.current_node.board).size
        outputs = np.zeros((data_size, move_count + 1))
        data_count = 0
        while True:
            self.search(self.current_node.board, iterations)
            assert self.current_node.children is not None
            assert self.current_node.child_predictions is not None
            move_weights = np.zeros(self.current_node.child_predictions.size)
            for child in self.current_node.children:
                move = child.move
                move_weights[move] = child.value_count
            total_weight = move_weights.sum()
            if total_weight:
                move_weights /= total_weight
            game_states.append([self.current_node.board, move_weights])
            move = np.random.choice(move_weights.size, p=move_weights)
            for child in self.current_node.children:
                if child.move == move:
                    self.current_node = child
                    break
            if self.game.is_ended(self.current_node.board):
                final_value, _ = self.heuristic.analyse(self.current_node.board)
                final_player = -self.game.get_active_player(self.current_node.board)
                for board, move_weights in game_states:
                    value = final_value
                    if self.game.get_active_player(board) != final_player:
                        value *= -1
                    boards[data_count] = self.game.get_spaces(board)
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


class MctsPlayer(Player):
    """ Use Monte Carlo Tree Search to choose moves in a game.

    This is based on the general discussion of MCTS in Wikipedia:
    https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    Also based on the specific adaptations of AlphaZero:
    http://web.stanford.edu/~surag/posts/alphazero.html
    The original AlphaZero paper:
    https://deepmind.com/blog/alphago-zero-learning-scratch/
    """
    DEFAULT_ITERATIONS = 80

    def __init__(self, game: Game,
                 player_number: int = Game.X_PLAYER,
                 iteration_count: int = DEFAULT_ITERATIONS,
                 heuristic: Heuristic = None):
        super().__init__(game, player_number, heuristic)
        self.iteration_count = iteration_count
        self.search_manager = SearchManager(game, self.heuristic)

    @property
    def heuristic(self) -> Heuristic:
        return self._heuristic

    @heuristic.setter
    def heuristic(self, value: Heuristic):
        self._heuristic = value
        search_manager = getattr(self, 'search_manager', None)
        if search_manager is not None:
            search_manager.heuristic = value

    def end_game(self, board: np.ndarray, opponent: Player):
        self.search_manager.reset()

    def choose_move(self, board: np.ndarray) -> int:
        """ Choose a move for the given board.

        :param board: an array of piece values, like the ones returned by
            game.create_board().
        :return: the chosen move's index in the list of valid moves.
        """
        self.search_manager.search(board, self.iteration_count)
        if self.game.get_move_count(board) < 15:
            return self.search_manager.choose_weighted_move()
        return self.search_manager.get_best_move()

    def get_move_probabilities(self, board: np.ndarray) -> typing.List[
            typing.Tuple[str, float, int, float]]:
        """ Report the probability that each move is the best choice.

        :param board: the board to analyse
        :return: [(move_display, probability, value_count, avg_value)], where
        value_count is the number of times the value was probed from the move,
        and avg_value is the average value from all those probes.
        """
        return self.search_manager.get_move_probabilities(board)

    def get_summary(self) -> typing.Sequence[str]:
        return (('mcts',) + tuple(self.heuristic.get_summary()) +
                (f'{self.iteration_count} iterations',))
