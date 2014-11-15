#! /usr/bin/env python3
from lib import config, database, download
from os.path import dirname, join

BASE_DIR = dirname(__file__)

blacklist, whitelist = config.read_config(join(BASE_DIR, 'config.json'))

for file_ in blacklist:
    data = download.download_file(file_)
    database.insert_blacklisted_domains('adaway.db', data, whitelist)

database.export_database(join(BASE_DIR, 'adaway.db'), 'hosts.txt')
