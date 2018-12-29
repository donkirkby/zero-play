import math
import typing
from random import choice

import numpy as np

from zero_play.game import Game


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
        self.win_rate = 0
        self.simulation_count = 0

    def __repr__(self):
        board_repr = " ".join(repr(self.board).split())
        board_repr = board_repr.replace('[ ', '[')
        return f"SearchNode({self.game!r}, {board_repr})"

    def __eq__(self, other):
        if isinstance(other, SearchNode):
            return np.array_equal(self.board, other.board)
        return NotImplemented

    def select_leaf(self):
        if self.simulation_count == 0:
            return self
        if self.children is None:
            self.children = self.find_all_children()
        if not self.children:
            return self

        # No neural network yet, so evenly distribute the prior values.
        prior = 1 / len(self.children)

        best_score = float('-inf')
        best_child = None
        for child in self.children:
            score = (self.exploration_weight * prior *
                     math.sqrt(self.simulation_count) /
                     (1+child.simulation_count))
            if score > best_score:
                best_score = score
                best_child = child
        return best_child.select_leaf()

    def find_all_children(self) -> typing.List['SearchNode']:
        children = []
        for move, is_valid in enumerate(self.game.get_valid_moves(self.board)):
            if is_valid:
                child_board = self.game.make_move(self.board, move)
                children.append(SearchNode(self.game,
                                           child_board,
                                           self,
                                           move))
        return children

    def record_value(self, value):
        self.win_rate = ((self.win_rate * self.simulation_count + value) /
                         (self.simulation_count + 1))
        self.simulation_count += 1
        if self.parent:
            self.parent.record_value(-value)

    def find_best_children(self):
        if self.children is None:
            self.children = self.find_all_children()
        best_win_rate = float('-inf')
        best_children = []
        for child in self.children:
            child_win_rate = child.win_rate
            if child_win_rate > best_win_rate:
                best_children = [child]
                best_win_rate = child_win_rate
            elif child_win_rate == best_win_rate:
                best_children.append(child)
        return best_children


class MctsPlayer:
    """ Use Monte Carlo Tree Search to choose moves in a game.

    This is based on the general discussion of MCTS in Wikipedia:
    https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    Also based on the specific adaptations of AlphaZero:
    http://web.stanford.edu/~surag/posts/alphazero.html
    The original AlphaZero paper:
    https://deepmind.com/blog/alphago-zero-learning-scratch/
    """
    def __init__(self, game: Game, iteration_count=800):
        self.game = game
        self.iteration_count = iteration_count

    def simulate(self, start_board: np.ndarray):
        if self.game.is_ended(start_board):
            winner = self.game.get_winner(start_board)
            active_player = self.game.get_active_player(start_board)
            previous_player = -active_player
            return winner * previous_player
        valid_moves, = np.nonzero(self.game.get_valid_moves(start_board))
        move = np.random.choice(valid_moves)
        next_board = self.game.make_move(start_board, move)
        return -self.simulate(next_board)

    def choose_move(self, board: np.ndarray) -> int:
        """ Choose a move for the given board.

        :param board: an array of piece values, like the ones returned by
            game.create_board().
        :return: the chosen move's index in the list of valid moves.
        """
        root = SearchNode(self.game, board)
        for _ in range(self.iteration_count):
            leaf = root.select_leaf()
            value = self.simulate(leaf.board)
            leaf.record_value(value)
        if root.children is None:
            root.select_leaf()
        best_children = root.find_best_children()
        child = choice(best_children)
        return child.move
