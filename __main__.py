#! /usr/bin/env python3
"""A python3 script to block publicity."""
from lib.config import Config
from lib.database import Database
from lib.validator import parse_args

args = parse_args()

config = Config()
config.create()

database = Database()
database.create()
database.populate()
database.export()
