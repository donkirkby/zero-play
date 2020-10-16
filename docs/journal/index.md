---
title: Journal
subtitle: How we got here
---
## 2018
In late [2018], I started the project and added the rules of Tic Tac Toe, plus a
basic MCTS player.

[2018]: 2018.md

## 2019
In [2019], I converted the [Shibumi Games] project to use this library, and
measured how win rates varied with MCTS iterations in several games. I tried
adding neural networks, but never really got them to be stronger than basic
MCTS with random playouts. I read several academic papers and books to try and
understand the tools better.

[2019]: 2019.md
[Shibumi Games]: https://github.com/donkirkby/shibumi-games

## 2020
### 19 Jul 2020
I took some of the ideas from my other projects around writing unit tests for
GUI code, and applied them to PySide2's `QGraphicsScene`. Most of it worked
pretty well, but the fonts were different between my workstation and TravisCI.
I also spent a long time tracking down PySide2's [installation bug]. Both of
those were easier to deal with once I set up the `travis-local.sh` script. One
idea: use `QGraphicsScene` for both the expected image and the actual image.

[installation bug]: https://bugreports.qt.io/browse/QTBUG-84749

### 3 Aug 2020
Actually got a GUI working with a playable Tic Tac Toe, then added Connect 4.
Connected an MCTS player to the GUI, and then added Othello.

After adding a review feature, I think the basic version is done. Before I go
back to fighting with machine learning, I'm going to try converting the Shibumi
project to use the new GUI.

### Sep 2020
Spargo has a superko rule that forbids any game state from being repeated. That
means that you have to track the current board state, as well as the history, so
I switched from board classes to game state classes.

Released the first usable release of this and Shibumi Games. One nice feature
is the adjustment of AI strength after wins and losses.

### Oct 2020
As the Shibumi games are gaining more controls, I decided to move most of the
controls out of the `QGraphicsScene`, so developers can use Qt's layout classes.
