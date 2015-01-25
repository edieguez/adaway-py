#! /usr/bin/env python3
import os
import sys
from argparse import ArgumentParser

import lib.config as config
import lib.database as database
import lib.termcolor as termcolor

# Argument parsing
parser = ArgumentParser(description='A python3 script to block publicity')
group = parser.add_mutually_exclusive_group()

group.add_argument('-a', action='store_true', help='apply blocking')
group.add_argument('-d', action='store_true', help='deactivate blocking')
group.add_argument('-u', action='store_true', help='update database')

args = parser.parse_args()

# Check if the user is root
if (os.getuid()):
    termcolor.write('This script needs root provileges :(', Font.RED)
    sys.exit(1)

config.write()
database.create()
database.populate()
database.export()
