#! /usr/bin/env python
"""A python3 script to block publicity."""

import os
import sys
from argparse import ArgumentParser

# Argument parsing
from lib.config import Config

parser = ArgumentParser(description='A python3 script to block publicity')
parser.add_argument('-o', dest='filename', help='output file')

group = parser.add_mutually_exclusive_group()
group.add_argument('-a', action='store_true', help='apply blocking')
group.add_argument('-d', action='store_true', help='deactivate blocking')
group.add_argument('-u', action='store_true', help='update database')

args = parser.parse_args()

singleton = Config()
print(singleton.filename)
