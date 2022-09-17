"""Manage the AdAway config file."""

import json
import os

from lib.termcolor import Termcolor

termcolor = Termcolor()


class Config:
    """An object to manage the AdAway configuration variables."""

    def __init__(self, hosts_file):
        """Create a new config object."""
        self.__base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.config = os.path.join(self.__base_dir, 'config.json')
        self.database = os.path.join(self.__base_dir, 'adaway.db')

        if hosts_file:
            self.hosts_file = hosts_file
        elif 'WINDIR' in os.environ:
            self.hosts_file = os.path.join(os.environ.get('WINDIR'), 'System32', 'Drivers', 'etc', 'hosts')
        else:
            self.hosts_file = '/etc/hosts'

    def read_key(self, key):
        """Read a key from the config file.

        Keyword arguments:
        key -- the key to read
        """
        return self._read()[key]

    def modify_key(self, key, value):
        current_config = self._read()

        if key in current_config:
            current_config[key] = value
            self._write(current_config)

    def file_exists(self):
        return os.path.exists(self.config)

    def write_default(self):
        """Create the default config file if not exists."""
        termcolor.info('Creating config file')

        raw_config = {
            'host_files': [
                'http://adaway.org/hosts.txt',
                'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext',
                'http://winhelp2002.mvps.org/hosts.txt',
                'http://someonewhocares.org/hosts/hosts'
            ],
            'blacklist': [
            ],
            'custom_hosts': {
            },
            'whitelist': [
            ]
        }

        self._write(raw_config)

    def _write(self, body) -> None:
        with open(self.config, 'w') as config_file:
            json.dump(body, config_file, indent=4)

    def _read(self) -> dict:
        with open(self.config) as raw_config:
            json_file = json.load(raw_config)

            return json_file
