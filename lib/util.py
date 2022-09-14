from argparse import ArgumentParser

from lib import database, file_util
from lib.config import Config


def parse_arguments():
    parser = ArgumentParser(description='A python3 script to block publicity')
    parser.add_argument('-o', dest='filename', help='output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', action='store_true', help='apply blocking')
    group.add_argument('-d', action='store_true', help='deactivate blocking')
    group.add_argument('-u', action='store_true', help='update database')

    return parser.parse_args()


def create_configuration():
    config = Config()

    if not config.file_exists():
        config.write_default()

    return config


def create_database():
    if not database.database_exists():
        database.create_default_database()


def populate_database():
    database.populate_database()


def export_hosts_file(filename):
    file_util.export_hosts_file(filename)
