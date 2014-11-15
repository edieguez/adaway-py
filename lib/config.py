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
        raw_config = \
            {
                "blacklist": [
                    "http://adaway.org/hosts.txt",
                    "http://hosts-file.net/ad_servers.asp",
                    "http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext",
                    "http://winhelp2002.mvps.org/hosts.txt",
                    "http://someonewhocares.org/hosts/hosts"
                ],
                "custom_host": {
                    "localhost": "127.0.0.1",
                    "ip6-localhost ip6-loopback": "::1"
                    "ip6-localnet": "fe00::0"
                    "ip6-mcastprefix": "ff00::0"
                    "ip6-allnodes": "ff02::1"
                    "ip6-allrouters": "ff02::2"
                },
                "whitelist": [
                    "adf.ly",
                    "localhost"
                ]
            }

        json.dump(raw_config, config_file, indent=4)
