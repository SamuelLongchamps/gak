from gak.interface import GakCommand
from gak.utils import list_configs


class ListGakCommand(GakCommand):
    def init_parser(self, subparsers):
        list_parser = subparsers.add_parser("list", aliases=['ls'],
                                            help="List configurations defined for this project")
        list_parser.set_defaults(func=self.command)

    def command(self, args, root):
        configs = list_configs(root)
        if configs:
            print("Configurations are defined for the following commands:")
            list(map(print, ("* {}".format(c.split(".")[0]) for c in configs)))
        else:
            print("No configuration defined!")
        return 0


GakCommand.register_command(ListGakCommand())
