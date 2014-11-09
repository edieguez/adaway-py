#! /usr/bin/env python3
from lib import config, database
from os.path import dirname, join

BASE_DIR = dirname(__file__)

ad_files, whitelist = config.read_config(join(BASE_DIR, 'config.json'))

print(ad_files)
print(whitelist)

database.insert_blacklisted_domains(join(BASE_DIR, 'adaway.db'), ad_files)
