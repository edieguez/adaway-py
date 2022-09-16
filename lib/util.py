from argparse import ArgumentParser

from lib import database, filesystem
from lib.config import Config


def parse_arguments():
    parser = ArgumentParser(description='A python3 script to block publicity')
    parser.add_argument('-o', dest='filename', help='output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', action='store_true', help='apply blocking')
    group.add_argument('-d', action='store_true', help='deactivate blocking')

    group.add_argument('-w', metavar='host', nargs='+', help='whitelist one or multiple hosts')
    group.add_argument('-b', metavar='host', nargs='+', help='blacklist one or multiple hosts')

    return parser.parse_args()


def apply_host_blocking(filename):
    _create_configuration()

    if not database.database_exists():
        database.create_default_database()
        _populate_database()

    _export_hosts_file(filename)


def deactivate_host_blocking(filename):
    _create_configuration()
    filesystem.export_hosts_headers(filename)


def fully_apply_host_blocking(filename):
    _create_configuration()

    if not database.database_exists():
        database.create_default_database()

    _populate_database()
    _export_hosts_file(filename)


def whitelist_hosts(filename: str, hosts: list) -> None:
    if hosts:
        config = _create_configuration()

        whitelist = set(config.read_key('whitelist'))
        whitelist.update(hosts)

        blacklist = set(config.read_key('blacklist'))
        blacklist = blacklist.difference(whitelist)

        config.modify_key('whitelist', sorted(whitelist))
        config.modify_key('blacklist', sorted(blacklist))

        apply_host_blocking(filename)


def blacklist_hosts(filename: str, hosts: list) -> None:
    if hosts:
        config = _create_configuration()

        blacklist = set(config.read_key('blacklist'))
        blacklist.update(hosts)

        whitelist = set(config.read_key('whitelist'))
        whitelist = whitelist.difference(blacklist)

        config.modify_key('whitelist', sorted(whitelist))
        config.modify_key('blacklist', sorted(blacklist))

        apply_host_blocking(filename)


def _create_configuration():
    config = Config()

    if not config.file_exists():
        config.write_default()

    return config


def _populate_database():
    database.populate_database()


def _export_hosts_file(filename):
    filesystem.export_hosts_file(filename)
