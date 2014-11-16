#! /usr/bin/env python3
from os import getuid, path
from sys import exit

from lib import config, database, download


if (getuid()):
    print('You aren\'t root and you never will be :(')
    exit(1)

BASE_DIR = path.dirname(__file__)
CONFIG = path.join(BASE_DIR, 'config.json')
DATABASE = path.join(BASE_DIR, 'adaway.db')

database.insert_blacklisted_domains(DATABASE, CONFIG)
database.export_database(DATABASE, CONFIG)
