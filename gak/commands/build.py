import os

from gak.interface import GakCommand
from gak.utils import retrieve_config


class BuildGakCommand(GakCommand):
    def init_parser(self, subparsers):
        build_parser = subparsers.add_parser("build", aliases=['b'],
                                             help="Build stuff")
        build_parser.add_argument("what", default="default", nargs="?", help="Stuff to build")
        build_parser.add_argument("-c", "--configure", action="store_true", help="Configure before building")
        build_parser.set_defaults(func=self.command)

    def command(self, args, root):
        config = retrieve_config("build", root)
        if not config:
            sys.stderr.write("No user configuration defined for 'build'\n")
            return 1

        default = config.get("default")
        if args.what == "?" and config:
            default_msg = ""
            if default:
                default_msg = " (default: {})".format(default)
                config.pop("default")

            print("Defined targets{}:".format(default_msg))
            list(map(print, ("* {}".format(k) for k in config.keys())))
            return 0

        if args.what == "default" and default:
            what = config.get(default)
            if not what:
                print("No configuration defined for default '{}'".format(default))
                return 1
        else:
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
