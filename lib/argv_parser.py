import argparse
from lib.name_generator import random_name


def parse_argv():
    parser = argparse.ArgumentParser(
        description='A simple Mafia game client'
    )

    parser.add_argument('server_address')

    parser.add_argument(
        '-u',
        '--username',
        help='username (if not provided, will be chosen at random)'
    )

    parser.add_argument(
        '-b',
        '--bot',
        action='store_true',
        help='if set, will run the client in bot mode (no user input)'
    )

    args = parser.parse_args()

    if args.username is None:
        args.username = random_name()

    return args
