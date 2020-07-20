import logging
import typing
from argparse import Namespace
from pathlib import Path

import numpy as np
from tensorflow.python.keras import Sequential, regularizers
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.python.keras.layers import Dense, Conv2D, Dropout, Flatten
from tensorflow.python.keras.models import load_model

from zero_play.game import GridGame
from zero_play.heuristic import Heuristic

logger = logging.getLogger(__name__)


class NeuralNet(Heuristic):
    def __init__(self, game: GridGame):
        super().__init__(game)
        # game params
        self.board_height = game.board_height
        self.board_width = game.board_width
        example_board = game.create_board()
        self.action_size = len(game.get_valid_moves(example_board))
        self.epochs_completed = 0
        self.epochs_to_train = 100
        args = Namespace(lr=0.001,
                         dropout=0.3,
                         epochs=10,
                         batch_size=64,
                         num_channels=512)
        self.checkpoint_name = 'random weights'
        self.args = args

        num_channels = 512
        kernel_size = [3, 3]
        dropout = 0.3
        model = Sequential()
        # regularizer = regularizers.l2(0.00006)
        regularizer = regularizers.l2(0.0001)
        model.add(Conv2D(num_channels,
                         kernel_size,
                         padding='same',
                         activation='relu',
                         input_shape=(self.board_height, self.board_width, 1),
                         activity_regularizer=regularizer))
        model.add(Conv2D(num_channels,
                         kernel_size,
                         padding='same',
                         activation='relu',
                         activity_regularizer=regularizer))
        model.add(Conv2D(num_channels,
                         kernel_size,
                         activation='relu',
                         activity_regularizer=regularizer))
        model.add(Conv2D(num_channels,
                         kernel_size,
                         activation='relu',
                         activity_regularizer=regularizer))
        model.add(Dropout(dropout))
        model.add(Dropout(dropout))
        model.add(Flatten())
        model.add(Dense(self.action_size + 1))
        model.compile('adam', 'mean_squared_error')
        self.model = model

    def get_summary(self) -> typing.Sequence[str]:
        return 'neural net', self.checkpoint_name

    def analyse(self, board: np.ndarray) -> typing.Tuple[float, np.ndarray]:
        if self.game.is_ended(board):
            return self.analyse_end_game(board)

        outputs = self.model.predict(self.game.get_spaces(board).reshape(
            (1,
             self.board_height,
             self.board_width,
             1)))

        policy = outputs[0, :-1]
        value = outputs[0, -1]

        return value, policy

    def get_path(self, folder):
        if folder is not None:
            folder_path = Path(folder)
        else:
            game_name = self.game.name.replace(' ', '-').lower()
            folder_path = Path('data') / game_name
        return folder_path

    def save_checkpoint(self, folder=None, filename='checkpoint.h5'):
        self.checkpoint_name = 'model ' + filename
        folder_path = self.get_path(folder)
        file_path = folder_path / filename
        folder_path.mkdir(parents=True, exist_ok=True)
        self.model.save(file_path)

    def load_checkpoint(self, folder=None, filename='checkpoint.h5'):
        self.checkpoint_name = 'model ' + filename
        folder_path = self.get_path(folder)
        file_path = folder_path / filename
        self.model = load_model(file_path)

    def train(self, boards: np.ndarray, outputs: np.ndarray, log_dir=None):
        """ Train the model on some sample data.

        :param boards: Each entry is a board position.
        :param outputs: Each entry is an array of policy values for the moves,
            as well as the estimated value of the board position.
        :param log_dir: Directory for TensorBoard logs. None disables logging.
        """

        if log_dir is None:
            callbacks = None
        else:
            callbacks = [TensorBoard(log_dir)]

        history = self.model.fit(
            np.expand_dims(boards, -1),
            outputs,
            verbose=0,
            initial_epoch=self.epochs_completed,
            epochs=self.epochs_completed+self.epochs_to_train,
            validation_split=0.2,
            callbacks=callbacks)
        self.epochs_completed += self.epochs_to_train
        return history
