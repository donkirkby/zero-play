import logging
import os
import typing
from argparse import Namespace

import numpy as np
import tensorflow as tf

from zero_play.game import Game
from zero_play.heuristic import Heuristic

logger = logging.getLogger(__name__)


class NeuralNet(Heuristic):
    def __init__(self, game: Game):
        super().__init__(game)
        # game params
        self.board_x, self.board_y = 7, 6
        self.action_size = 7
        args = Namespace(lr=0.001,
                         dropout=0.3,
                         epochs=10,
                         batch_size=64,
                         num_channels=512)
        self.args = args

        # Renaming functions
        Relu = tf.nn.relu
        Tanh = tf.nn.tanh
        BatchNormalization = tf.layers.batch_normalization
        Dropout = tf.layers.dropout
        Dense = tf.layers.dense

        # Neural Net
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.input_boards = tf.placeholder(tf.float32, shape=[None, self.board_y, self.board_x])    # s: batch_size x board_x x board_y
            self.dropout = tf.placeholder(tf.float32)
            self.isTraining = tf.placeholder(tf.bool, name="is_training")

            x_image = tf.reshape(self.input_boards, [-1, self.board_y, self.board_x, 1])                    # batch_size  x board_x x board_y x 1
            h_conv1 = Relu(BatchNormalization(self.conv2d(x_image, args.num_channels, 'same'), axis=3, training=self.isTraining))      # batch_size  x board_x x board_y x num_channels
            h_conv2 = Relu(BatchNormalization(self.conv2d(h_conv1, args.num_channels, 'same'), axis=3, training=self.isTraining))      # batch_size  x board_x x board_y x num_channels
            h_conv3 = Relu(BatchNormalization(self.conv2d(h_conv2, args.num_channels, 'valid'), axis=3, training=self.isTraining))     # batch_size  x (board_x-2) x (board_y-2) x num_channels
            h_conv4 = Relu(BatchNormalization(self.conv2d(h_conv3, args.num_channels, 'valid'), axis=3, training=self.isTraining))     # batch_size  x (board_x-4) x (board_y-4) x num_channels
            h_conv4_flat = tf.reshape(h_conv4, [-1, args.num_channels * (self.board_y - 4) * (self.board_x - 4)])
            s_fc1 = Dropout(Relu(BatchNormalization(Dense(h_conv4_flat, 1024), axis=1, training=self.isTraining)), rate=self.dropout)  # batch_size x 1024
            s_fc2 = Dropout(Relu(BatchNormalization(Dense(s_fc1, 512), axis=1, training=self.isTraining)), rate=self.dropout)          # batch_size x 512
            self.pi = Dense(s_fc2, self.action_size)                                                        # batch_size x self.action_size
            self.prob = tf.nn.softmax(self.pi)
            self.v = Tanh(Dense(s_fc2, 1))                                                               # batch_size x 1

            self.calculate_loss()
        self.sess = tf.Session(graph=self.graph)
        with tf.Session() as temp_sess:
            temp_sess.run(tf.global_variables_initializer())
        self.sess.run(tf.variables_initializer(self.graph.get_collection('variables')))
        self.saver = None

    def conv2d(self, x, out_channels, padding):
        return tf.layers.conv2d(x, out_channels, kernel_size=[3, 3], padding=padding)

    def calculate_loss(self):
        self.target_pis = tf.placeholder(tf.float32, shape=[None, self.action_size])
        self.target_vs = tf.placeholder(tf.float32, shape=[None])
        self.loss_pi = tf.losses.softmax_cross_entropy(self.target_pis, self.pi)
        self.loss_v = tf.losses.mean_squared_error(self.target_vs, tf.reshape(self.v, shape=[-1, ]))
        self.total_loss = self.loss_pi + self.loss_v
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            self.train_step = tf.train.AdamOptimizer(self.args.lr).minimize(self.total_loss)

    def analyse(self, board: np.ndarray) -> typing.Tuple[float, np.ndarray]:
        if self.game.is_ended(board):
            return self.analyse_end_game(board)
        # preparing input
        board = board[np.newaxis, :, :]

        # run
        prob, v = self.sess.run([self.prob, self.v], feed_dict={self.input_boards: board, self.dropout: 0, self.isTraining: False})

        return float(v[0][0]), prob[0]

    def save_checkpoint(self, folder='data/connect4-nn', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        if self.saver is None:
            self.saver = tf.train.Saver(self.graph.get_collection('variables'))
        with self.graph.as_default():
            self.saver.save(self.sess, filepath)

    def load_checkpoint(self, folder='data/connect4-nn', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        with self.graph.as_default():
            self.saver = tf.train.Saver()
            self.saver.restore(self.sess, filepath)

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, policy, value)
        """

        for epoch in range(self.args.epochs):
            batch_idx = 0

            # self.sess.run(tf.local_variables_initializer())
            batch_count = int(len(examples) / self.args.batch_size)
            while batch_idx < batch_count:
                sample_ids = np.random.randint(len(examples), size=self.args.batch_size)
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))

                # predict and compute gradient and do SGD step
                input_dict = {self.input_boards: boards, self.target_pis: pis, self.target_vs: vs, self.dropout: self.args.dropout, self.isTraining: True}

                # record loss
                self.sess.run(self.train_step, feed_dict=input_dict)
                pi_loss, v_loss = self.sess.run([self.loss_pi, self.loss_v], feed_dict=input_dict)
                logger.info('Batch %d of %d: pi_loss %f, v_loss %f.',
                            batch_idx,
                            batch_count,
                            pi_loss,
                            v_loss)

                batch_idx += 1
