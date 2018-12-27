from abc import ABC, abstractmethod

import numpy as np


class Game(ABC):
    DISPLAY_CHARS = 'O.X'
    NO_PLAYER = 0
    X_PLAYER = 1
    O_PLAYER = -1

    @abstractmethod
    def create_board(self, text: str = None) -> np.ndarray:
        pass

    @abstractmethod
    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        pass

    def is_ended(self, board: np.ndarray) -> bool:
        if self.get_winner(board) != self.NO_PLAYER:
            return True
        valid_moves = self.get_valid_moves(board)
        return not valid_moves.any()

    @abstractmethod
    def display(self, board: np.ndarray, show_coordinates: bool = False) -> str:
        pass

    @abstractmethod
    def display_move(self, move: int) -> str:
        pass

    @abstractmethod
    def parse_move(self, text: str) -> int:
        pass

    def display_player(self, player: int) -> str:
        if player == self.X_PLAYER:
            return 'Player X'
        return 'Player O'

    def get_active_player(self, board: np.ndarray) -> int:
        x_count = (board == self.X_PLAYER).sum()
        y_count = (board == self.O_PLAYER).sum()
        return self.X_PLAYER if x_count == y_count else self.O_PLAYER

    @abstractmethod
    def make_move(self, board: np.ndarray, move: int) -> np.ndarray:
        pass

    def get_winner(self, board: np.ndarray) -> int:
        for player in (self.X_PLAYER, self.O_PLAYER):
            if self.is_win(board, player):
                return player

        return self.NO_PLAYER

    @abstractmethod
    def is_win(self, board: np.ndarray, player: int) -> bool:
        pass
