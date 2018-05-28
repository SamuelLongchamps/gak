import subprocess

from gak.interface import GakCommand
from gak.utils import retrieve_user_config


class MkdevGakCommand(GakCommand):
    def init_parser(self, subparsers):
        mkdev_parser = subparsers.add_parser("mkdev", aliases=["md"],
                                             help="Rename the current branch with a dev prefix")
        mkdev_parser.add_argument("-t", "--toggle", action="store_true",
                                  help="Toggle between the dev prefix")
        mkdev_parser.set_defaults(func=self.command)

    def command(self, args, root):
        user_config = retrieve_user_config()
        prefix = user_config.get("mkdev", {}).get("prefix")
        if not prefix:
            print("[WARNING] No dev prefix defined, default to 'dev'")
            prefix = "dev"

        current_branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
        split_current_branch = current_branch.split("/")
        is_dev_branch = split_current_branch[0] == prefix

        cmd = None
        if not is_dev_branch:
            cmd = "git branch -m {current} {prefix}/{current}".format(
                current=current_branch, prefix=prefix)
        elif args.toggle:
            cmd = "git branch -m {prefix}/{suffix} {suffix}".format(
                prefix=prefix, suffix=split_current_branch[1])

        if cmd:
            print(cmd)
            result = subprocess.getoutput(cmd)
            if result:
                print(result)
            return 0
        else:
            print("Nothing to do, already prefixed by {}".format(prefix))
        return 1


GakCommand.register_command(MkdevGakCommand())
