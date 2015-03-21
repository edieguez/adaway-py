"""Manage the AdAway config file."""

import json
import os
import sys

from lib.termcolor import Termcolor, Font

termcolor = Termcolor()


def get_filename():
    """Get the hosts file name for Linux or Windows."""
    if 'WINDIR' in os.environ:
        FILENAME = os.path.join(
            os.environ.get('WINDIR'), 'System32', 'Drivers', 'etc', 'hosts')
    else:
        FILENAME = '/etc/hosts'

    return FILENAME


def read(key):
    """Read a key from the config file.

    Keyword arguments:
    key -- the key value to be readed
    """
    with open(CONFIG) as raw_config:
        json_file = json.load(raw_config)

        return json_file[key]


def write():
    """Create the default config file if not exists."""
    if os.path.exists(CONFIG):
        return

    termcolor.write('[!] Creating config file', Font.GREEN)

    with open(CONFIG, 'w') as config_file:
        raw_config = {
            'host_files': [
                'http://adaway.org/hosts.txt',
                'http://hosts-file.net/ad_servers.asp',
                'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext',
                'http://winhelp2002.mvps.org/hosts.txt',
                'http://someonewhocares.org/hosts/hosts'
            ],
            'blacklist': [
            ],
            'custom_hosts': {
            },
            'whitelist': [
                'adf.ly',
                'www.linkbucks.com'
            ]
        }

        json.dump(raw_config, config_file, indent=4)


termcolor.write("Importando el modulo de configuracion", Font.CYAN)
__BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG = os.path.join(__BASE_DIR, 'config.json')
DATABASE = os.path.join(__BASE_DIR, 'adaway.db')
FILENAME = get_filename()
