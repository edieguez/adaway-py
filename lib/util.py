from argparse import ArgumentParser

from lib import filesystem
from lib import network
from lib.config import Config, termcolor
from lib.database import Database


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
    config = _create_configuration()
    database = Database(config.database)

    if not database.database_exists():
        termcolor.warn('Creating default database')
        database.create_default_database()

        for hosts in _download_host_files(config.read_key('host_files')):
            database.populate_database(hosts)

    whitelisted_hosts = config.read_key('whitelist')
    _export_hosts_file(filename, database.get_blocked_hosts(whitelisted_hosts), config.read_key('blacklist'))


def _download_host_files(host_files):
    for host_file in host_files:
        yield network.download_file(host_file)


def deactivate_host_blocking(filename):
    _create_configuration()
    filesystem.export_hosts_headers(filename)


def fully_apply_host_blocking(filename):
    config = _create_configuration()
    database = Database(config.database)

    if not database.database_exists():
        termcolor.warn('Creating default database')
        database.create_default_database()

    for hosts in _download_host_files(config.read_key('host_files')):
        database.populate_database(hosts)

    whitelisted_hosts = config.read_key('whitelist')
    _export_hosts_file(filename, database.get_blocked_hosts(whitelisted_hosts), config.read_key('blacklist'))


def whitelist_hosts(filename: str, hosts: list) -> None:
    config = _create_configuration()

    whitelist = set(config.read_key('whitelist'))
    whitelist.update(hosts)

    blacklist = set(config.read_key('blacklist'))
    blacklist = blacklist.difference(whitelist)

    config.modify_key('whitelist', sorted(whitelist))
    config.modify_key('blacklist', sorted(blacklist))

    apply_host_blocking(filename)


def blacklist_hosts(filename: str, hosts: list) -> None:
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


def _export_hosts_file(filename, blocked_hosts, blacklisted_hosts):
    filesystem.export_hosts_file(filename, blocked_hosts, blacklisted_hosts)
