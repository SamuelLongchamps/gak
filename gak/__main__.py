import os
import sys

from argparse import ArgumentParser
from glob import glob

from gak.interface import GakCommand
import gak.utils as utils


def find_commands():
    # Go through the commands directory, import all files
    lookup = os.path.join(os.path.dirname(__file__), "commands", "*.py")
    command_modules = glob(lookup)
    for cm in command_modules:
        module = "gak.commands.{}".format(os.path.basename(cm)[:-3])
        __import__(module, locals(), globals())


def main():
    main_parser = ArgumentParser()

    subparsers = main_parser.add_subparsers(dest="subname", help="Action to take")

    find_commands()
    for commands in GakCommand.ALL_COMMANDS:
        commands.init_parser(subparsers)

    args = main_parser.parse_args()

    if not args.subname:
        main_parser.print_usage()
        exit(0)

    root = utils.get_repo_root()
    if not root:
        sys.stderr.write("Not in a git repo\n")
        exit(1)

    try:
        result = args.func(args, root)
    except KeyboardInterrupt:
        result = 1

    sys.exit(result)


if __name__ == "__main__":
    main()
