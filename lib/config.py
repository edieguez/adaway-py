import json
import os

import lib.termcolor as termcolor


__BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG = os.path.join(__BASE_DIR, 'config.json')
DATABASE = os.path.join(__BASE_DIR, 'adaway.db')

def read(key):
    with open(CONFIG) as raw_config:
        json_file = json.load(raw_config)

        return json_file[key]

def write():
    if os.path.exists(CONFIG):
        return

    with open(CONFIG, 'w') as config_file:
        raw_config = {
            'host_files': [
                'http://adaway.org/hosts.txt',
                #'http://hosts-file.net/ad_servers.asp',
                #'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext',
                #'http://winhelp2002.mvps.org/hosts.txt',
                #'http://someonewhocares.org/hosts/hosts'
            ],
            'blacklist': [
                'youtube.com'
            ],
            'custom_hosts': {
                'saegusa': '128.0.0.1'
            },
            'whitelist': [
                'adf.ly',
                'www.linkbucks.com'
            ]
        }

        json.dump(raw_config, config_file, indent=4)
