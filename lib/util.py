from argparse import ArgumentParser

from lib import filesystem
from lib import network
from lib.config import Config, termcolor
from lib.database import Database


def parse_arguments():
    parser = ArgumentParser(description='A python3 script to block ads using the hosts file')
    parser.add_argument('-o', dest='hosts_file', help='output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', action='store_true', help='apply blocking')
    group.add_argument('-d', action='store_true', help='deactivate blocking')

    group.add_argument('-w', metavar='host', nargs='+', help='whitelist one or multiple hosts')
    group.add_argument('-W', metavar='host', nargs='+', help='remove from white list one or multiple hosts')
    group.add_argument('-b', metavar='host', nargs='+', help='blacklist one or multiple hosts')
    group.add_argument('-B', metavar='host', nargs='+', help='remove from black list one or multiple hosts')

    return parser.parse_args()


def apply_host_blocking(hosts_file):
    config = _create_configuration(hosts_file)
    database = Database(config.database)

    if not database.database_exists():
        termcolor.warn('Creating default database')
        database.create_default_database()

        for hosts in _download_host_files(config.read_key('host_files')):
            database.populate_database(hosts)

    custom_hosts = config.read_key('custom_hosts')
    whitelisted_hosts = config.read_key('whitelist')
    blocked_hosts = database.get_blocked_hosts(whitelisted_hosts)
    blacklisted_hosts = config.read_key('blacklist')

    _export_hosts_file(config.hosts_file, custom_hosts, blocked_hosts, blacklisted_hosts)


def _download_host_files(host_files):
    for host_file in host_files:
        yield network.download_file(host_file)


def deactivate_host_blocking(hosts_file):
    config = _create_configuration(hosts_file)
    custom_hosts = config.read_key('custom_hosts')

    filesystem.export_hosts_headers(config.hosts_file, custom_hosts)


def fully_apply_host_blocking(hosts_file):
    config = _create_configuration(hosts_file)
    database = Database(config.database)

    if not database.database_exists():
        termcolor.warn('Creating default database')
        database.create_default_database()

    for hosts in _download_host_files(config.read_key('host_files')):
        database.populate_database(hosts)

    custom_hosts = config.read_key('custom_hosts')
    whitelisted_hosts = config.read_key('whitelist')
    blocked_hosts = database.get_blocked_hosts(whitelisted_hosts)
    blacklisted_hosts = config.read_key('blacklist')

    _export_hosts_file(config.hosts_file, custom_hosts, blocked_hosts, blacklisted_hosts)


def whitelist_hosts(hosts_file: str, hosts: list) -> None:
    config = _create_configuration(hosts_file)

    whitelist = set(config.read_key('whitelist'))
    whitelist.update(hosts)

    blacklist = set(config.read_key('blacklist'))
    blacklist = blacklist.difference(whitelist)

    config.modify_key('whitelist', sorted(whitelist))
    config.modify_key('blacklist', sorted(blacklist))

    apply_host_blocking(hosts_file)


def remove_whitelisted_hosts(hosts_file: str, hosts: list) -> None:
    config = _create_configuration(hosts_file)

    whitelist = set(config.read_key('whitelist'))
    whitelist = whitelist.difference(hosts)

    config.modify_key('whitelist', sorted(whitelist))

    apply_host_blocking(hosts_file)


def blacklist_hosts(hosts_file: str, hosts: list) -> None:
    config = _create_configuration(hosts_file)

    blacklist = set(config.read_key('blacklist'))
    blacklist.update(hosts)

    whitelist = set(config.read_key('whitelist'))
    whitelist = whitelist.difference(blacklist)

    config.modify_key('whitelist', sorted(whitelist))
    config.modify_key('blacklist', sorted(blacklist))

    apply_host_blocking(hosts_file)


def remove_blacklisted_hosts(hosts_file: str, hosts: list) -> None:
    config = _create_configuration(hosts_file)

    blacklist = set(config.read_key('blacklist'))
    blacklist = blacklist.difference(hosts)

    config.modify_key('blacklist', sorted(blacklist))

    apply_host_blocking(hosts_file)


def _create_configuration(hosts_file):
    config = Config(hosts_file)

    if not config.file_exists():
        config.write_default()

    return config


def _export_hosts_file(hosts_file, custom_hosts, blocked_hosts, blacklisted_hosts):
    filesystem.export_hosts_file(hosts_file, custom_hosts, blocked_hosts, blacklisted_hosts)
