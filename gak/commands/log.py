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
	class LogGakCommand(GakCommand):
		def init_parser(self, subparsers):
			log_parser = subparsers.add_parser("log", help="Log time to Jira for a task")
			log_parser.add_argument("to_log", help="Log to apply")
			log_parser.add_argument("issue", nargs="?", help="Issue ID (XX-####), defaults to current branch prefix (element before the first underscore)")
			log_parser.add_argument("-m", "--message", help="Message for the worklog")
			log_parser.set_defaults(func=self.command)

		def command(self, args, root):
			if not args.issue:
				# Default to the prefix of the current branch name
				args.issue = subprocess.getoutput("git rev-parse --abbrev-ref HEAD").split('_')[0]

			print("About to log in issue {}".format(args.issue))

			jira = connect_to_jira()
			if not jira:
				return 1

			try:
				jira.add_worklog(args.issue, args.to_log, comment=args.message)
				print("Successfully logged {} in issue {}{}".format(args.to_log, args.issue, " with mention '{}'".format(args.message) if args.message else ""))
			except JIRAError as e:
				sys.stderr.write("Could not log (Code {})".format(e.status_code))
				return 1


	GakCommand.register_command(LogGakCommand())
