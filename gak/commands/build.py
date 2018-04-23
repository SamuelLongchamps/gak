import os

from gak.interface import GakCommand
from gak.utils import retrieve_config


class BuildGakCommand(GakCommand):
    def init_parser(self, subparsers):
        build_parser = subparsers.add_parser("build", aliases=['p'],
                                             help="Build stuff")
        build_parser.add_argument("what", help="Stuff to build")
        build_parser.add_argument("-c", "--configure", action="store_true", help="Configure before building")
        build_parser.set_defaults(func=self.command)

    def command(self, args, root):
        config = retrieve_config("build", root)
        what = config.get(args.what)
        if what is not None:
            if args.configure or args.what == "configure":
                config_commands = config.get("configure")
                if config_commands:
                    for cc in config_commands:
                        os.system(cc.format(root=root))
                else:
                    print("No configure step defined in the build configuration")

            if what:
                if args.what != "configure":
                    for w in what:
                        build_cmd = w.format(root=root)
                        os.system(build_cmd)
                return 0
            else:
                print("Nothing defined to build!")
        else:
            print("No configuration defined for '{}'".format(args.what))
        return 1


GakCommand.register_command(BuildGakCommand())
