
class GakCommand:
    ALL_COMMANDS = []
    """:type: list[GakCommand]"""

    @staticmethod
    def register_command(instance):
        assert isinstance(instance, GakCommand)
        GakCommand.ALL_COMMANDS.append(instance)

    def init_parser(self, subparsers):
        """
        :param subparsers: Subparsers manager to which a subparser can be added
        """
        raise NotImplementedError()

    def command(self, args, root):
        """
        :param args: Arguments provided by the user for the command
        :param root: Root to the Git repository the command was launched from
        :return: Code of the application (0 for success, non-zero for error)
        """
        raise NotImplementedError()
