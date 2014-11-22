#! /usr/bin/env python3
from os import getuid, path
from sys import exit

from lib import config, database, download
from lib.termcolor import Background, Font, Format, FormatPrinter


if (getuid()):
    print('You aren\'t root and you never will be :(')
    exit(1)

BASE_DIR = path.dirname(__file__)
CONFIG = path.join(BASE_DIR, 'config.json')
DATABASE = path.join(BASE_DIR, 'adaway.db')

writer = FormatPrinter()

if not path.exists(CONFIG):
    writer.write('    [!] Creating default config file', Font.GREEN)
    config.write_default_config(CONFIG)

if not path.exists(DATABASE):
    writer.write('    [!] Creating database file', Font.GREEN)
    database.create_database(DATABASE)

blacklist_files = config.read_config(CONFIG, 'blacklist')

for file_ in blacklist_files:
    writer.write('    [!] Downloading %s' % file_, Font.GREEN)
    blacklist = download.download_file(file_)
    database.insert_blacklisted_domains(DATABASE, blacklist)

custom_hosts, whitelist = config.read_config(CONFIG, 'custom_hosts', 'whitelist')

writer.write('    [!] Creating hosts file', Font.GREEN)
database.export_database(DATABASE, custom_hosts, whitelist)
