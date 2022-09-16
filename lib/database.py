import os
import sqlite3
from sqlite3 import Cursor

from lib.filesystem import config, termcolor
from lib.network import download_file


def database_exists():
    """Returns True if the file exists, otherwise returns False"""
    return os.path.exists(config.database)


def create_default_database():
    """Create a new database"""
    termcolor.info('Creating database')

    with sqlite3.connect(config.database) as connection:
        cursor = connection.cursor()

        sql = (
            'CREATE TABLE blacklist ('
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
                    cursor.execute('INSERT INTO blacklist VALUES(?)', (host,))
                except sqlite3.IntegrityError:
                    pass


def get_blocked_hosts() -> Cursor:
    whitelist = config.read_key('whitelist')
    whitelist.append('localhost')

    with sqlite3.connect(config.database) as connection:
        cursor = connection.cursor()

        return cursor.execute(
            f'''SELECT hostname FROM blacklist
            WHERE hostname NOT IN ({','.join(['?'] * len(whitelist))})
            ORDER BY hostname''', whitelist
        )
