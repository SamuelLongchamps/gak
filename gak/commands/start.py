import os
import sys
import subprocess

from gak.interface import GakCommand

try:
    from jira import JIRA, JIRAError
    from gak.jira_utils import connect_to_jira
except:
    pass
else:
    class StartGakCommand(GakCommand):
        def init_parser(self, subparsers):
            start_parser = subparsers.add_parser("start", help="Start a task by creating a branch with an appropriate name")
            start_parser.add_argument("issue", nargs="?", help="Issue ID (XX-####) or JIRA URL to issue")
            start_parser.add_argument("-b", "--branch", default="master", help="Branch name from which to branch")
            start_parser.add_argument("--here", action='store_true', help="Do not checkout to master and pull, checkout from the current branch")
            start_parser.add_argument("--prefix", "-p", type=str, help="Prefix to add to the new branch name")
            start_parser.set_defaults(func=self.command)

        def command(self, args, root):
            jira = connect_to_jira(True)
            if not jira:
                return 1

            if "/" in args.issue:
                # Handle as a URL
                args.issue = args.issue.split("/")[-1]

            if not args.here:
                completed = subprocess.run("git checkout {}".format(args.branch))
                if completed.returncode != 0:
                    return 1
                completed = subprocess.run("git pull")
                if completed.returncode != 0:
                    return 1

            try:
                issue = jira.issue(args.issue, "summary")
                print("Creating branch for issue '{}'".format(issue.fields.summary))
                suffix = input("Enter branch suffix name: ")
                if not suffix:
                    sys.stderr.write("No branch provided, aborting.")
                    return 1

                branch_name = "{}_{}".format(args.issue, suffix)
                branch_name = branch_name.replace(" ", "_")  # Safety to prevent any weird stuff
                branch_prefix = "/" + args.prefix.replace(" ", "_") if args.prefix else ""

                subprocess.run("git checkout -b {}{}".format(branch_prefix, branch_name))

            except JIRAError as e:
                sys.stderr.write("Could not fetch issue '{}' (Code {})".format(args.issue, e.status_code))
                return 1


    GakCommand.register_command(StartGakCommand())
