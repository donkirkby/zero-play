### 21 Dec 2018 ###
I found the [alpha-zero-general project] very helpful to learn the ideas in the
[AlphaGo Zero paper], but I have some different ideas for the project
structure and API. I've decided to write a new library using the same ideas.

[alpha-zero-general project]: https://github.com/suragnair/alpha-zero-general
[AlphaGo Zero paper]: https://deepmind.com/blog/alphago-zero-learning-scratch/

### 26 Dec 2018 ###
I've got Tic Tac Toe implemented, because it's nice and small for writing unit
tests. So far, it's only the game logic and a human player interface.
I also added Connect 4 as a slightly deeper game that can have more interesting
board positions than Tic Tac Toe.

### 29 Dec 2018 ###
Basic Monte Carlo Tree Search is now working! There's no neural network yet.
I ended up just using a tree structure for the search nodes, so I don't need
all the hash tables that alpha-zero-general used.

I plotted the win rates of two MCTS players with different numbers of search
iterations, and the pattern was as expected. The more searching, the higher the
win rate. You can see that there's a slight advantage for the first player, and
player 1's win rate is 64% when both players search with 128 simulations.

The gradient isn't as smooth when both players use fewer than 10 simulations,
but they're basically making random moves at that point.

![MCTS win rate]

[MCTS win rate]: 2018/connect-4-wins-mcts.png

### 2 Jan 2019 ###
I added an entry point in `setup.py` for other projects to define game rules.
Using that entry point within the Zero Play library, I plotted the win rates of
two MCTS players playing Tic Tac Toe:

![Tic Tac Toe win rate]

You can seee the same general trends as in Connect 4. I'm not sure what's
happening in the bottom right.

Using the same entry point in my [Shibumi project], I converted the Spline game
to use the new Zero Play library, and plotted the win rates:

![Spline win rate]

[Tic Tac Toe win rate]: 2019/tictactoe-wins.png
[Shibumi project]: https://github.com/donkirkby/shibumi-games
[Spline win rate]: 2019/spline-wins.png

### 4 Jan 2019 ###
I found a bug in the MCTS code that selects which nodes to expand. It wasn't
taking advantage of the win rates to explore the more successful positions.

With that fixed, the problems at low iterations have gone away:

![Fixed Connect 4 win rate]

![Fixed Spline win rate]

![Fixed Tic Tac Toe win rate]

I'm not sure what's happening with high simulation count for Tic Tac Toe's
first player, but everything else looks beautiful now.

[Fixed Connect 4 win rate]: 2019/connect4-win-rate.png
[Fixed Spline win rate]: 2019/spline-win-rate.png
[Fixed Tic Tac Toe win rate]: 2019/tictactoe-win-rate.png

### 12 Jan 2019 ###
Added the first version of code to train a neural network, and I added a system
so that game and player classes from other projects can add arguments to the
command line. See the `CommandParser` class in `zero_play.py`.
