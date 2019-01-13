from unittest.mock import patch, Mock

from pkg_resources import EntryPoint

from zero_play.human_player import HumanPlayer
from zero_play.tictactoe.game import TicTacToeGame
from zero_play.zero_play import CommandParser, EntryPointArgument


class DummyGame:
    DEFAULT_SIZE = 'large'

    size = EntryPointArgument('-s',
                              help='size of dummy game',
                              default=DEFAULT_SIZE)

    def __init__(self, size: str):
        self.size = size


def test_entry_point():
    parser = CommandParser()
    parser.add_argument('game', action='entry_point')

    args = parser.parse_args(['tictactoe'])
    game = parser.load_argument(args, 'game')

    assert 'tictactoe' == args.game
    assert isinstance(game, TicTacToeGame)


def test_entry_point_default():
    parser = CommandParser()
    parser.add_argument('--game', action='entry_point', default='tictactoe')

    args = parser.parse_args([])
    game = parser.load_argument(args, 'game')

    assert isinstance(game, TicTacToeGame)


def test_entry_point_value():
    parser = CommandParser()
    parser.add_argument('--game', action='entry_point', nargs='*')

    args = parser.parse_args(['--game', 'connect4', 'tictactoe'])
    game = parser.load_argument(args, 'game', args.game[1])

    assert isinstance(game, TicTacToeGame)


def test_extra_attributes():
    parser = CommandParser()
    parser.add_argument('game', action='entry_point')
    parser.add_argument('--player', '-p', action='entry_point')

    args = parser.parse_args(['tictactoe', '-p', 'human'])
    game = parser.load_argument(args, 'game')
    player = parser.load_argument(args, 'player', game=game)

    assert isinstance(game, TicTacToeGame)
    assert isinstance(player, HumanPlayer)
    assert player.game is game


@patch('zero_play.zero_play.iter_entry_points')
@patch('pkg_resources.EntryPoint.require', new=Mock())
def test_duplicate_entry_name(mock_entry_points):
    mock_entry_points.return_value = [
        EntryPoint.parse('dummy=test_parser:DummyGame'),
        EntryPoint.parse('dummy=zero_play.tictactoe.game:TicTacToeGame')]
    parser = CommandParser(prog='zero_play')
    parser.add_argument('game', action='entry_point')
    expected_help_text = """\
usage: zero_play [-h] [--size SIZE] {dummy,dummy-2}

positional arguments:
  {dummy,dummy-2}

optional arguments:
  -h, --help            show this help message and exit
  --size SIZE, -s SIZE  size of dummy game
"""

    help_text = parser.format_help()

    assert expected_help_text == help_text


@patch('zero_play.zero_play.iter_entry_points')
@patch('pkg_resources.EntryPoint.require', new=Mock())
def test_load_duplicate(mock_entry_points):
    mock_entry_points.return_value = [
        EntryPoint.parse('dummy=test_parser:DummyGame'),
        EntryPoint.parse('dummy=zero_play.tictactoe.game:TicTacToeGame')]
    parser = CommandParser()
    parser.add_argument('game', action='entry_point')

    args = parser.parse_args(['dummy-2'])
    game = parser.load_argument(args, 'game')

    assert isinstance(game, TicTacToeGame)


@patch('zero_play.zero_play.iter_entry_points')
@patch('pkg_resources.EntryPoint.require', new=Mock())
def test_extra_argument_help(mock_entry_points):
    mock_entry_points.return_value = [
        EntryPoint.parse('dummy=test_parser:DummyGame'),
        EntryPoint.parse('tictactoe=zero_play.tictactoe.game:TicTacToeGame')]
    parser = CommandParser(prog='zero_play')
    parser.add_argument('game', action='entry_point')
    expected_help_text = """\
usage: zero_play [-h] [--size SIZE] {dummy,tictactoe}

positional arguments:
  {dummy,tictactoe}

optional arguments:
  -h, --help            show this help message and exit
  --size SIZE, -s SIZE  size of dummy game
"""

    help_text = parser.format_help()

    assert expected_help_text == help_text


@patch('zero_play.zero_play.iter_entry_points')
@patch('pkg_resources.EntryPoint.require', new=Mock())
def test_extra_argument_ignored(mock_entry_points):
    mock_entry_points.return_value = [
        EntryPoint.parse('dummy=test_parser:DummyGame'),
        EntryPoint.parse('tictactoe=zero_play.tictactoe.game:TicTacToeGame')]
    parser = CommandParser()
    parser.add_argument('game', action='entry_point')

    args = parser.parse_args(['tictactoe'])
    game = parser.load_argument(args, 'game')

    assert not hasattr(game, 'size')


@patch('zero_play.zero_play.iter_entry_points')
@patch('pkg_resources.EntryPoint.require', new=Mock())
def test_extra_argument_assigned(mock_entry_points):
    mock_entry_points.return_value = [
        EntryPoint.parse('dummy=test_parser:DummyGame'),
        EntryPoint.parse('tictactoe=zero_play.tictactoe.game:TicTacToeGame')]
    parser = CommandParser()
    parser.add_argument('game', action='entry_point')

    args = parser.parse_args(['dummy'])
    game = parser.load_argument(args, 'game')

    assert DummyGame.DEFAULT_SIZE == game.size
