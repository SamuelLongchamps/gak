import subprocess
import fnmatch

from gak.interface import GakCommand
from gak.utils import retrieve_config, to_platform_path


class SwitchGakCommand(GakCommand):
    def init_parser(self, subparsers):
        switch_parser = subparsers.add_parser("switch", aliases=["s", "sw"],
                                              help="Interactive branch switching using wildcard")
        switch_parser.add_argument("wildcard", nargs="?", default="?", type=str, help="Wildcard of branch name")
        switch_parser.set_defaults(func=self.command)

    def command(self, args, root):
        branches = subprocess.getoutput("git branch")
        """:type: str"""

        if args.wildcard == "?":
            print(subprocess.getoutput("git branch"))
            return 0

        # Use wildcard search that supports any content before or after (much like grep)
        pattern = "*{}*".format(args.wildcard)

        target_branches = fnmatch.filter(
            filter(lambda branch: not branch.startswith("*"), branches.splitlines()),
            pattern
        )

        if target_branches:
            # Trim any space
            target_branches = [x.lstrip(" ") for x in target_branches]

            if len(target_branches) > 1:
                list(map(print, ("{}) {}".format(idx, branch)
                                 for idx, branch in zip(range(len(target_branches)),
                                                        target_branches))))
                value = input("Choose a branch (non-number to cancel): ")
            else:
                value = "n" \
                    if input("Switch to branch '{}'? (Yes: Enter, No: Any): ".format(target_branches[0])) \
                    else "0"

            if value.isdigit():
                value_int = int(value)
                if 0 <= value_int < len(target_branches):
                    cmd = "git checkout {}".format(target_branches[value_int])
                    print(cmd)
                    result = subprocess.getoutput(cmd)
                    if result:
                        print(result)
                else:
                    print("Value '{}' is not an option.".format(value_int))
            else:
                print("Operation canceled.")
            return 0
        else:
            print("No branch matching pattern '{}'".format(pattern))

        return 1


GakCommand.register_command(SwitchGakCommand())
