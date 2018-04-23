import os
import sys

from gak.interface import GakCommand
from gak.utils import retrieve_config, to_platform_path


class ToGakCommand(GakCommand):
    def init_parser(self, subparsers):
        to_parser = subparsers.add_parser("to", help="Go to places in the repo")
        to_parser.add_argument("place", help="Place to go to")
        to_parser.set_defaults(func=self.command)

    def command(self, args, root):
        config = retrieve_config("to", root)

        # Add default places
        config.update({
            "root": ""
        })

        if args.place == "?":
            print("Defined values:")
            for k, v in config.items():
                print("* {} =>\t{}".format(k, to_platform_path(os.path.join(root, v))))
            return 0

        target = config.get(args.place)
        if target is not None:
            target_platform_path = os.path.join(root, target)
            sys.stdout.write(to_platform_path(target_platform_path))
            return 0
        else:
            print("No target called '{}' defined in the repository configuration".format(args.place))
        return 1


GakCommand.register_command(ToGakCommand())
