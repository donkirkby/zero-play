from argparse import ArgumentDefaultsHelpFormatter

from zero_play.command import play, train, plot_strengths
from zero_play.command_parser import CommandParser


def create_parser():
    parser = CommandParser(formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(title='subcommands')
    play.create_parser(subparsers)
    plot_strengths.create_parser(subparsers)
    train.create_parser(subparsers)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    args.handle(args)


if __name__ == '__main__':
    main()
