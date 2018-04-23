import os
import sys
import json
import subprocess

CONFIG_FOLDER = "gakconfig.d"
USER_CONFIG_FILE = "~/.gakconfig.json"
IS_MINGW = False

def detect_mingw():
    global IS_MINGW
    IS_MINGW = subprocess.getoutput("uname").startswith("MINGW")
    return IS_MINGW


def to_platform_path(os_path):
    if IS_MINGW:
        os_path = os_path.replace('\\', '/')
        if os_path[1] == ':':
            os_path = "/{}/{}".format(os_path[0].lower(), os_path[3:])
    return os_path


def get_repo_root():
    try:
        result = subprocess.getoutput("git rev-parse --show-toplevel").split(' ')[0]
        return None if result == "fatal:" else result
    except subprocess.CalledProcessError as e:
        pass


def retrieve_user_config():
    try:
        expanded_path = os.path.expanduser(USER_CONFIG_FILE)
        with open(expanded_path) as f:
            return json.load(f)
    except IOError:
        sys.stderr.write("No user config file '{}'\n".format(USER_CONFIG_FILE))
    except json.decoder.JSONDecodeError:
        sys.stderr.write("Unable to read the user configuration file '{}'\n".format(USER_CONFIG_FILE))

    return {}


def retrieve_config(action, root=None):
    root = root or get_repo_root()
    if not root:
        return {}

    config_filepath = "{}.json".format(os.path.join(root, CONFIG_FOLDER, action))
    try:
        with open(config_filepath) as f:
            return json.load(f)
    except IOError:
        sys.stderr.write("No configuration file '{}'\n".format(config_filepath))
    except json.decoder.JSONDecodeError:
        sys.stderr.write("Unable to read the configuration file '{}'\n".format(config_filepath))

    return {}


def list_configs(root=None):
    root = root or get_repo_root()
    if not root:
        return []

    config_folder = os.path.join(root, CONFIG_FOLDER)
    if not os.path.exists(config_folder):
        return []

    # Only json files are configuration files
    return filter(lambda p: os.path.splitext(p)[1] == ".json", os.listdir(os.path.join(root, CONFIG_FOLDER)))


# Initialization
detect_mingw()
