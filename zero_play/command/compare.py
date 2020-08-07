import json
from argparse import ArgumentParser
from pathlib import Path

from zero_play.command.play import PlayController
from zero_play.command_parser import CommandParser
from zero_play.game import Game
from zero_play.mcts_player import MctsPlayer


def parse_args():
    parser = ArgumentParser(description='Compare the strengths of two players.')
    # noinspection PyTypeChecker
    parser.add_argument('scenario',
                        type=Path,
                        help="JSON file to record a scenario, if the JSON and "
                             "CSV files already exist, they will be plotted")
    parser.add_argument('--continue',
                        action='store_true',
                        help='continue writing to an existing file')
    return parser.parse_args()


def choose(prompt, choices, default=None):
    if default is None:
        default = choices[0]
    displays = choices[:]
    displays[0] = f'[{displays[0]}]'
    choice_list = ', '.join(displays)
    chosen = input(f'{prompt} {choice_list} ')
    if chosen == '':
        chosen = default
    return chosen


def choose_scenario(scenario_path: Path) -> PlayController:
    parser = CommandParser()
    game_entries = parser.load_group('game')
    game_names = sorted(game_entries)
    game_name = choose('Choose the game:', game_names)
    game_class = game_entries[game_name]
    game = game_class()

    heuristic_entries = parser.load_group('heuristic')
    heuristic_names = sorted(heuristic_entries)
    heuristic1_name = choose('Choose a heuristic for player 1:',
                             heuristic_names)
    heuristic1_class = heuristic_entries[heuristic1_name]
    heuristic1 = heuristic1_class(game)
    heuristic2_name = choose('Choose a heuristic for player 2:',
                             heuristic_names)
    heuristic2_class = heuristic_entries[heuristic2_name]
    heuristic2 = heuristic2_class(game)

    description = input('Enter a scenario description: ')

    scenario_text = json.dumps(dict(command='compare',
                                    description=description,
                                    game=game_name,
                                    heuristic=[heuristic1_name,
                                               heuristic2_name]))
    scenario_path.write_text(scenario_text)

    player1 = MctsPlayer(game, Game.X_PLAYER, heuristic=heuristic1)
    player2 = MctsPlayer(game, Game.O_PLAYER, heuristic=heuristic2)
    return PlayController(game, [player1, player2])


def main():
    args = parse_args()
    scenario_path: Path = args.scenario.with_suffix('.json')
    controller = choose_scenario(scenario_path)
    print(controller.game.name)


if __name__ == '__main__':
    main()
