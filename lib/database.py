import os
import sqlite3

from lib.file_util import config, termcolor
from lib.network import download_file


def database_exists():
    """Returns True if the file exists, otherwise returns False"""
    return os.path.exists(config.database)


def create_default_database():
    """Create a new database"""
    termcolor.info('Creating dabatase')

    with sqlite3.connect(config.database) as connection:
        cursor = connection.cursor()

        sql = (
            'CREATE TABLE blacklist ('
            '    id INTEGER NOT NULL PRIMARY KEY,'
            '    hostname TEXT NOT NULL UNIQUE'
            ');'
        )

        cursor.execute(sql)


def populate_database():
    """Populate the database using hosts files as source."""
    host_files = config.read_key('host_files')

    for host_file in host_files:
        hosts = download_file(host_file)

        with sqlite3.connect(config.database) as connection:
            cursor = connection.cursor()

            for host in hosts:
                try:
                    cursor.execute('INSERT INTO blacklist VALUES(NULL, ?)', (host,))
                except sqlite3.IntegrityError:
                    pass


def get_blocked_hosts() -> list:
    whitelist = config.read_key('whitelist')
    whitelist.append('localhost')

    with sqlite3.connect(config.database) as connection:
        cursor = connection.cursor()

        hosts = cursor.execute('SELECT hostname FROM blacklist')
        hosts = set([host[0] for host in hosts])

        return sorted(hosts.difference(whitelist))
