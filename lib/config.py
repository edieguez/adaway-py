import json
from os.path import exists

def read_config(config_file):
    if not exists(config_file):
        write_default_config(config_file)

    blacklist = list()
    whitelist = list()

    with open(config_file) as raw_config:
        json_file = json.load(raw_config)
        blacklist = json_file['blacklist']
        whitelist = json_file['whitelist']

    return blacklist, whitelist

def write_default_config(filename):
    with open(filename, 'w') as config_file:
        raw_config = (
            '{\n'
            '    "blacklist": [\n'
            '        "http://adaway.org/hosts.txt",\n'
            '        "http://hosts-file.net/ad_servers.asp",\n'
            '        "http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext",\n'
            '        "http://winhelp2002.mvps.org/hosts.txt",\n'
            '        "http://someonewhocares.org/hosts/hosts"\n'
            '    ],\n'
            '    "whitelist": [\n'
            '        "adf.ly",\n'
            '        "localhost"\n'
            '    ]\n'
            '}'
        )

        config_file.write(raw_config)
