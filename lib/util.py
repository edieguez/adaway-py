from argparse import ArgumentParser

from lib import database, file_util
from lib.config import Config


def parse_arguments():
    parser = ArgumentParser(description='A python3 script to block publicity')
    parser.add_argument('-o', dest='filename', help='output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', action='store_true', help='apply blocking')
    group.add_argument('-d', action='store_true', help='deactivate blocking')

    return parser.parse_args()


def apply_host_blocking(filename):
    _create_configuration()

    if not database.database_exists():
        database.create_default_database()
        _populate_database()

    _export_hosts_file(filename)


def deactivate_host_blocking(filename):
    _create_configuration()
    file_util.export_hosts_headers(filename)


def fully_apply_host_blocking(filename):
    _create_configuration()

    if not database.database_exists():
        database.create_default_database()

    _populate_database()
    _export_hosts_file(filename)


def _create_configuration():
    config = Config()

    if not config.file_exists():
        config.write_default()

    return config


def _populate_database():
    database.populate_database()


def _export_hosts_file(filename):
    file_util.export_hosts_file(filename)
