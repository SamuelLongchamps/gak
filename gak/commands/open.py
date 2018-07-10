import sys

import os

from gak.interface import GakCommand
from gak.utils import retrieve_config, retrieve_user_config


class OpenGakCommand(GakCommand):
    def init_parser(self, subparsers):
        open_parser = subparsers.add_parser("open", aliases=['o'], help="Open stuff")
        open_parser.add_argument("what", default="default", nargs="?", help="Stuff to open")
        open_parser.set_defaults(func=self.command)

    def command(self, args, root):
        config = retrieve_config("open", root)
        user_config = retrieve_user_config()
        open_user_config = user_config.get("open")
        if not open_user_config:
            sys.stderr.write("No user configuration defined for 'open'\n")
            return 1

        if args.what == "?":
            default_msg = ""
            default = config.get("default")
            if default:
                default_msg = " (default: {})".format(default)
                config.pop("default")

            print("Defined targets{}:".format(default_msg))
            list(map(print, ("* {} => opens through '{}'".format(k, v[0]) for k, v in config.items())))
            return 0

        if args.what == "default":
            args.what = config.get("default")

        what = config.get(args.what)
        if what is not None:
            runner = open_user_config.get(what[0])

            if " " in what[1]:
                # Complex case, do a formatting of the root
                target = what[1].format(root=root)
            else:
                # Simple case, just prepend the root
                target = os.path.join(root, what[1])

            print("Opening {}".format(target))
            os.system(runner.format(target))
            return 0
        return 1


GakCommand.register_command(OpenGakCommand())
