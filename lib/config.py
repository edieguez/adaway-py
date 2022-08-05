"""Manage the AdAway config file."""

import json
import os

from lib.termcolor import Termcolor

termcolor = Termcolor()


class Config:
    """An object to manage the AdAway configuration variables."""

    def __init__(self):
        """Create a new config object."""
        self.__BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.CONFIG = os.path.join(self.__BASE_DIR, 'config.json')
        self.DATABASE = os.path.join(self.__BASE_DIR, 'adaway.db')
        self.FILENAME = self.get_filename()

    @staticmethod
    def get_filename():
        """Get the hosts file name for Linux/Mac OS or Windows."""
        if 'WINDIR' in os.environ:
            FILENAME = os.path.join(
                os.environ.get('WINDIR'), 'System32', 'Drivers', 'etc', 'hosts')
        else:
            FILENAME = '/etc/hosts'

        return FILENAME

    def read(self, key):
        """Read a key from the config file.

        Keyword arguments:
        key -- the key value to be readed
        """
        with open(self.CONFIG) as raw_config:
            json_file = json.load(raw_config)

            return json_file[key]

    def write(self):
        """Create the default config file if not exists."""
        if os.path.exists(self.CONFIG):
            return

        termcolor.info('Creating config file')

        with open(self.CONFIG, 'w') as config_file:
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
