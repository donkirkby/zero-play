# Zero Play [![Build Status Badge]][latest build] #
## Teach a computer to play any game. ##

[Build Status Badge]: https://travis-ci.org/donkirkby/zero-play.svg?branch=master
[latest build]: https://travis-ci.org/donkirkby/zero-play

The zero play library is based on the ideas in the [AlphaGo Zero paper] and the
example Python code in the [alpha-zero-general project]. The goal of this
project is to make a reusable Python library that other projects can build on
to make powerful computer opponents for many different board games.

The main command is `zero_play`, and it has a few subcommands. Run
`zero_play -h` to see a list of subcommands.

### Play subcommand ###
It has options for the game, and which players to pit against each other.
One game is Tic Tac Toe.

    $ zero_play play tictactoe
      ABC
    1 ...
    2 ...
    3 ...
    
      ABC
    1 ...
    2 .X.
    3 ...
    Player O:

Another game is Connect 4.

    $ zero_play play connect4
    1234567
    .......
    .......
    .......
    .......
    .......
    .......
    
    1234567
    .......
    .......
    .......
    .......
    .......
    ...X...
    Player O: 

Use `zero_play play -h` to list all the options.

### Train subcommand ###
This trains a neural network, and reports its progress.

    $ zero_play train connect4
    2019-01-13 11:53:15.239988: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
    2019-01-13 11:53:15,864 INFO:zero_play.command.train: Creating training data.
    2019-01-13 11:53:30,568 DEBUG:zero_play.mcts_player: Created 21 training examples so far.
    2019-01-13 11:53:57,135 DEBUG:zero_play.mcts_player: Created 60 training examples so far.
    2019-01-13 11:54:41,388 DEBUG:zero_play.mcts_player: Created 125 training examples so far.
    2019-01-13 11:55:44,720 INFO:zero_play.command.train: Training for checkpoint-00.pth.tar.
    2019-01-13 11:55:47,645 INFO:zero_play.connect4.neural_net: Batch 0 of 3: pi_loss 1.924198, v_loss 0.810040.
    2019-01-13 11:55:49,195 INFO:zero_play.connect4.neural_net: Batch 1 of 3: pi_loss 1.985169, v_loss 1.056920.
    2019-01-13 11:55:50,709 INFO:zero_play.connect4.neural_net: Batch 2 of 3: pi_loss 2.047058, v_loss 1.608997.
    [...]
    2019-01-13 11:56:29,302 INFO:zero_play.connect4.neural_net: Batch 0 of 3: pi_loss 1.655714, v_loss 0.973489.
    2019-01-13 11:56:30,841 INFO:zero_play.connect4.neural_net: Batch 1 of 3: pi_loss 1.571650, v_loss 1.075505.
    2019-01-13 11:56:32,365 INFO:zero_play.connect4.neural_net: Batch 2 of 3: pi_loss 1.630466, v_loss 1.038757.
    Checkpoint Directory exists! 
    2019-01-13 11:56:33,060 INFO:zero_play.command.train: Creating training data.
    2019-01-13 11:56:40,365 DEBUG:zero_play.mcts_player: Created 11 training examples so far.
    [...]

### Plot subcommand ###
This plots the strengths of the two players, as we adjust the number of search
iterations. Run `zero_play plot -h` for a list of options.


I'm planning to keep a [journal] for the project.

[AlphaGo Zero paper]: https://deepmind.com/blog/alphago-zero-learning-scratch/
[alpha-zero-general project]: https://github.com/suragnair/alpha-zero-general
[journal]: docs/journal/