#! /usr/bin/env python3
from lib import config


ad_files, white_list = config.read_config('config.json')

print(ad_files)
print(white_list)
