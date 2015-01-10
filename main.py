#! /usr/bin/env python3
from argparse import ArgumentParser
from os import getuid, path
from sys import exit

from lib import config, database, download
from lib.termcolor import Background, Font, Format, write


# Argument parsing
parser = ArgumentParser(description='A python3 script to block publicity')
group = parser.add_mutually_exclusive_group()

group.add_argument('-a', action='store_true', help='apply blocking')
group.add_argument('-d', action='store_true', help='deactivate blocking')
group.add_argument('-u', action='store_true', help='update database')

args = parser.parse_args()

# Check if the user is root
if (getuid()):
    write('This script needs root provileges :(', Font.RED)
    exit(1)

# Basic variables
BASE_DIR = path.dirname(__file__)
CONFIG = path.join(BASE_DIR, 'config.json')
DATABASE = path.join(BASE_DIR, 'adaway.db')

if not path.exists(CONFIG):
    write('    [!] Creating default config file', Font.GREEN)
    config.write_default_config(CONFIG)

custom_hosts, whitelist = config.read_config(CONFIG, 'custom_hosts', 'whitelist')

if args.d:
    write('    [!] Deactivating blocking', Font.GREEN)
    database.export_database(custom_hosts)

    exit(0)

if not path.exists(DATABASE):
    write('    [!] Creating database file', Font.GREEN)
    database.create_database(DATABASE)

    args.a = False

if not args.a:
    blacklist_files = config.read_config(CONFIG, 'blacklist')

    for file_ in blacklist_files:
        write('    [!] Downloading %s' % file_, Font.GREEN)
        blacklist = download.download_file(file_)
        database.insert_blacklisted_domains(DATABASE, blacklist)

if not args.u:
    write('    [!] Creating hosts file', Font.GREEN)
    database.export_database(custom_hosts, whitelist, DATABASE)
