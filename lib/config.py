"""Manage the AdAway config file."""

import json
import os


class Config:
    instance = None

    def __new__(cls):
        if not Config.instance:
            Config.instance = Config.__config()

        return Config.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)

    class __config:
        def __init__(self):
            self.__BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            self.config = os.path.join(self.__BASE_DIR, 'config.json')
            self.database = os.path.join(self.__BASE_DIR, 'adaway.db')

        @property
        def filename(self):
            if 'WINDIR' in os.environ:
                filename = os.path.join(
                    os.environ.get('WINDIR'), 'System32', 'Drivers', 'etc', 'hosts')
            else:
                filename = '/etc/hosts'

            return filename

        def read(self, key):
            """Read a key from the config file.
        
            Keyword arguments:
            key -- the key value to be readed
            """
            with open(self.config) as raw_config:
                json_file = json.load(raw_config)

                return json_file[key]

        def write(self):
            """Create the default config file if not exists."""
            if os.path.exists(Config):
                return

            with open(self.config, 'w') as config_file:
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
