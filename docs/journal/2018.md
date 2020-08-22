# Project Journal
### 21 Dec 2018
I found the [alpha-zero-general project] very helpful to learn the ideas in the
[AlphaGo Zero paper]. (Use the link at the bottom of the page.) I have some
different ideas for the project structure and API, so I've decided to write a
new library using the same ideas.

[alpha-zero-general project]: https://github.com/suragnair/alpha-zero-general
[AlphaGo Zero paper]: https://deepmind.com/blog/alphago-zero-learning-scratch/

### 26 Dec 2018
I've got Tic Tac Toe implemented, because it's nice and small for writing unit
tests. So far, it's only the game logic and a human player interface.
I also added Connect 4 as a slightly deeper game that can have more interesting
board positions than Tic Tac Toe.

### 29 Dec 2018
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

### 2 Jan 2019
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

### 4 Jan 2019
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

### 12 Jan 2019
Added the first version of code to train a neural network, and I added a system
so that game and player classes from other projects can add arguments to the
command line. See the `CommandParser` class in `zero_play.py`.

### 16 Feb 2019
Two main tasks in the last month: the neural network sort of works, and I
configured Tensorflow to use the GPU. The GPU configuration was a giant pain,
again! I had it working a few months ago, but it stopped working for some
reason. I did the original setup based on a [GPU tutorial] that shows how
to install multiple driver versions: one that's compatible with my display
and the operating system, and another that's compatible with Tensorflow. After
a bunch of investigation I described in this [GPU question] on Stack Overflow,
I figured out that I had two driver versions squished together in one location.
With a bunch of clean up, I got it working again. The GPU version is about 12
times faster than the CPU version.

As for actually using the neural network, it's not very impressive yet. I
found a new way to display the skill of a player, by comparing it to several
strengths of a basic MCTS player using simple playouts to value board
positions.

![Connect 4 win rates with neural network]

Here, the blue and green lines show a basic MCTS player using simple playouts
and 80 search iterations for each move. The blue line is the win rate as player
1 against the same player with increasing numbers of search iterations. The
green line is the win rate as player 2. Unsurprisingly, both win rates drop as
the opponent strength increases.

The sad part is that the win rates are actually *lower* when I switch from
using simple playouts to using a neural network to value the board positions.
The purple and pink lines use the same number of iterations, but use a neural
network instead of playouts.

In contrast, just increasing the search iterations from 80 to 128 makes the
player stronger.

![Connect 4 win rates with 128 iterations]

Here, all the players are using simple playouts. The player with 128 search
iterations does better than 80 search iterations, and much better than the
neural network.

I'll try to run the same tests on the alpha-zero-general project to see if
their neural network is actually helpful.

[Connect 4 win rates with 128 iterations]: 2019/connect4-128-win-rate.png 
[Connect 4 win rates with neural network]: 2019/connect4nn-win-rate.png 

[GPU tutorial]: https://blog.kovalevskyi.com/multiple-version-of-cuda-libraries-on-the-same-machine-b9502d50ae77
[GPU question]: https://stackoverflow.com/q/54567427/4794

### 22 Feb 2019
I tried running the alpha-zero-general project's Connect 4 player against my
basic player without a neural network, and it was at least no worse than my
basic player.

![Connect 4 win rates in alpha-zero-general]

Something must be wrong with my neural network or my training, so I'm reading
the original [AlphaGo Zero paper]. (The link at the bottom of the page gives
free access.) One difference I noticed is that I haven't implemented the idea
of temperature in my loss function.

Also, their loss function uses mean squared error for the values, but cross
entropy for the move policies. I use mean squared error for everything. I don't
know if I can mix things like that in the high-level API I'm using.

[Connect 4 win rates in alpha-zero-general]: 2019/connect4-general-nn.png

### 26 Feb 2019
I've been reading the AlphaGo Zero paper, and I found the [AlphaZero paper]
(includes an open-access link). The [AlphaZero supplementary material] even
includes some Python code as pseudocode for the algorithm! In that pseudocode,
it looks like the player uses softmax sampling to choose a move for the first
30 moves of a game, then uses the best move from then on. I think this is
related to the temperature algorithm I saw in the other paper.

[AlphaZero paper]: https://deepmind.com/blog/alphazero-shedding-new-light-grand-games-chess-shogi-and-go/
[AlphaZero supplementary material]: http://science.sciencemag.org/content/suppl/2018/12/05/362.6419.1140.DC1

### 28 Nov 2019
Since the machine learning was so frustrating, I started working on a PySide2
user interface. I just experimented with some ideas in the designer, but I
didn't really hook them up to anything.

### 19 Jul 2020
I took some of the ideas from my other projects around writing unit tests for
GUI code, and applied them to PySide2's `QGraphicsScene`. Most of it worked
pretty well, but the fonts were different between my workstation and TravisCI.
I also spent a long time tracking down PySide2's [installation bug].

[installation bug]: https://bugreports.qt.io/browse/QTBUG-84749

### 3 Aug 2020
Actually got a GUI working with a playable Tic Tac Toe, then added Connect 4.
Connected an MCTS player to the GUI, and then added Othello.

After adding a review feature, I think the basic version is done. Before I go
back to fighting with machine learning, I'm going to try converting the Shibumi
project to use the new GUI.
