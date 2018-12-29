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
