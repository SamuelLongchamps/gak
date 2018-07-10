import sys

from getpass import getpass
from jira import JIRA, JIRAError

from gak.utils import retrieve_user_config


def connect_to_jira(is_anonymous=False):
    user_config = retrieve_user_config()
    user_config_jira = user_config.get("jira")

    if not user_config_jira:
        sys.stderr.write("No user configuration defined for 'jira'\n")
        return None

    if is_anonymous:
        anon = user_config_jira.get("anonymous", {})
        username = anon.get("username")
        password = anon.get("password")
    else:
        username = user_config_jira.get("username")
        password = None

    if not username:
        sys.stderr.write("No username defined in user configuration of 'jira'{}\n".format(" (anonymous)" if is_anonymous else ""))
        return None

    server = user_config_jira.get("server")
    if not server:
        sys.stderr.write("No server defined in user configuration of 'jira'\n")
        return None

    if not password:
        # Basic authentication only for now...
        try:
            password = getpass("Enter the password for '{}': ".format(username))
        except EOFError:
            sys.stderr.write("No password provided, aborting.")
            return None

    try:
        jira = JIRA({"server": server}, basic_auth=(username, password))
        return jira
    except JIRAError as e:
        sys.stderr.write("Could not connect to JIRA (Code {})".format(e.status_code))
