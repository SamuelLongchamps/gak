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
	class CommitGakCommand(GakCommand):
		def init_parser(self, subparsers):
			commit_parser = subparsers.add_parser("commit", help="Commit the staged area with a prepared message based on the branch name and corresponding JIRA issue")
			commit_parser.add_argument("-m", "--message", help="Pass a message directly, do not open the editor")
			commit_parser.set_defaults(func=self.command)

		def command(self, args, root):
			# Default to the prefix of the current branch name
			issue = subprocess.getoutput("git rev-parse --abbrev-ref HEAD").split('/')[-1].split('_')[0]

			jira = connect_to_jira(True) # anonymous
			if not jira:
				return 1

			try:
				issue = jira.issue(issue, "summary")
				
				header = "{} {}".format(issue, issue.fields.summary)
				print("Commit for issue {}".format(header))
				
				command = "git commit -m \"{}\n\n{}\"{}".format(
					header,
					args.message if args.message else "",
					"" if args.message else " -e",
				)

				subprocess.run(command)

			except JIRAError as e:
				sys.stderr.write("Could not fetch issue '{}' (Code {})".format(issue, e.status_code))
				return 1
	
	GakCommand.register_command(CommitGakCommand())
