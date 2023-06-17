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
In [2020], I switched to a GUI using PySide, and supported multiprocessing.
I published the first release on PyPI.

[2020]: 2020.md

## 2021
### Mar 2021
Plot opponent strength over time as it adjusts to wins and losses.

## 2023
### Apr 2023
Restore the tool to plot win rates between different numbers of MCTS iterations.

### May 2023
Switch MCTS search to limit by time instead of iterations, since that will make
more sense when comparing neural network with random playouts.
