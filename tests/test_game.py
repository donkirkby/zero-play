from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from unittest.mock import patch, Mock

import pytest
from pkg_resources import EntryPoint

from zero_play.connect4.game import Connect4Game
from zero_play.game import Game


def test_help():
    parser = ArgumentParser(prog='some_command',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    Game.add_argument(parser)
    expected_help = """\
usage: some_command [-h] [-g {connect4,tictactoe}]

optional arguments:
  -h, --help            show this help message and exit
  -g {connect4,tictactoe}, --game {connect4,tictactoe}
                        the game to play (default: tictactoe)
"""

    help_text = parser.format_help()

    assert expected_help == help_text


def test_load():
    game = Game.load('connect4')

    assert game is Connect4Game


def test_load_unknown():
    with pytest.raises(ValueError, match=r"Unknown game: 'does-not-exist'\."):
        Game.load('does-not-exist')


@patch('zero_play.game.iter_entry_points')
def test_duplicate_choices(mock_entry_points):
    mock_entry_points.return_value = [
        EntryPoint.parse('tictactoe=zero_play.tictactoe.game:TicTacToeGame'),
        EntryPoint.parse('tictactoe=zero_play.connect4.game:Connect4Game')]
    parser = ArgumentParser(prog='some_command',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    Game.add_argument(parser)
    expected_help = """\
usage: some_command [-h] [-g {tictactoe,tictactoe-2}]

optional arguments:
  -h, --help            show this help message and exit
  -g {tictactoe,tictactoe-2}, --game {tictactoe,tictactoe-2}
                        the game to play (default: tictactoe)
"""

    help_text = parser.format_help()

    assert expected_help == help_text


@patch('zero_play.game.iter_entry_points')
@patch('pkg_resources.EntryPoint.require', new=Mock())
def test(mock_entry_points):
    mock_entry_points.return_value = [
        EntryPoint.parse('tictactoe=zero_play.tictactoe.game:TicTacToeGame'),
        EntryPoint.parse('tictactoe=zero_play.connect4.game:Connect4Game')]

    game = Game.load('tictactoe-2')

    assert Connect4Game is game
