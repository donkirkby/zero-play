import logging
import typing
from argparse import Namespace
from pathlib import Path

import numpy as np
# noinspection PyUnresolvedReferences
from tensorflow.keras import optimizers
# noinspection PyUnresolvedReferences
from tensorflow.keras import Sequential, regularizers
# noinspection PyUnresolvedReferences
from tensorflow.keras.callbacks import TensorBoard
# noinspection PyUnresolvedReferences
from tensorflow.keras.layers import Dense, Conv2D, Dropout, Flatten
# noinspection PyUnresolvedReferences
from tensorflow.keras.models import load_model
from tensorflow.python.keras.callbacks import EarlyStopping

from zero_play.game_state import GridGameState, GameState
from zero_play.heuristic import Heuristic

logger = logging.getLogger(__name__)


class NeuralNet(Heuristic):
    def __init__(self, start_state: GameState) -> None:
        if not isinstance(start_state, GridGameState):
            raise ValueError(f'{start_state.__class__} is not a subclass of GridGameState.')
        super().__init__()
        # start_state params
        self.board_height = start_state.board_height
        self.board_width = start_state.board_width
        self.action_size = len(start_state.get_valid_moves())
        self.epochs_completed = 0
        self.epochs_to_train = 100
        self.start_state = start_state
        args = Namespace(lr=0.001,
                         dropout=0.3,
                         epochs=10,
                         batch_size=64,
                         num_channels=512)
        self.checkpoint_name = 'random weights'
        self.args = args

        num_channels = 64
        kernel_size = [3, 3]
        regularizer = regularizers.l2(0.0001)
        input_shape = (2, self.board_height, self.board_width, 1)
        model = Sequential(
            [Conv2D(num_channels,
                    kernel_size,
                    padding='same',
                    activation='relu',
                    input_shape=input_shape,
                    activity_regularizer=regularizer),
             Flatten(),
             Dense(64, activation='relu'),
             Dense(64, activation='relu'),
             Dense(self.action_size + 1)])
        model.compile(loss='mean_absolute_error',
                      optimizer=optimizers.Adam(0.001))
        self.model = model

    def get_summary(self) -> typing.Sequence[str]:
        return 'neural net', self.checkpoint_name

    def analyse(self, board: GameState) -> typing.Tuple[float, np.ndarray]:
        if board.is_ended():
            return self.analyse_end_game(board)

        outputs = self.model(board.spaces.reshape(
            (1, 2, self.board_height, self.board_width, 1))).numpy()

        policy = outputs[0, :-1]
        value = outputs[0, -1]

        return value, policy

    def get_path(self, folder):
        if folder is not None:
            folder_path = Path(folder)
        else:
            game_name = self.start_state.game_name.replace(' ', '-').lower()
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

    def train(self, boards: np.ndarray, outputs: np.ndarray):
        """ Train the model on some sample data.

        :param boards: Each entry is a board position.
        :param outputs: Each entry is an array of policy values for the moves,
            as well as the estimated value of the board position.
        """

        self.checkpoint_name += ' + training'

        callbacks = [EarlyStopping(patience=10)]

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
