"""Manage the AdAway database."""

import operator
import os
import sqlite3
from socket import gethostname

from lib.config import Config
from lib.download import download_file
from lib.termcolor import Termcolor

config = Config()
termcolor = Termcolor()


def create():
    """Create a new database.

    returns True if the file exists, otherwise returns False.
    """
    if os.path.exists(config.DATABASE):
        return True

    termcolor.info('Creating dabatase')

    with sqlite3.connect(config.DATABASE) as connection:
        cursor = connection.cursor()
        sql = (
            'CREATE TABLE blacklist ('
            '    id INTEGER NOT NULL PRIMARY KEY,'
            '    hostname TEXT NOT NULL UNIQUE'
            ');'
        )
        cursor.execute(sql)
        return False


def populate():
    """Populate the database using hosts files as source."""
    host_files = config.read('host_files')

    for host_file in host_files:
        hosts = download_file(host_file)

        with sqlite3.connect(config.DATABASE) as connection:
            cursor = connection.cursor()

            for host in hosts:
                try:
                    cursor.execute('INSERT INTO blacklist VALUES(NULL, ?)', (host,))
                except sqlite3.IntegrityError:
                    pass


def export(filename=None, deactivate=False):
    """Export the database to a text file.

    Keyword arguments:
    filename -- The file where the database will be exported
    deactivate -- If True the blocking will be deactivated
    """
    filename = filename or config.FILENAME

    with open(filename, 'w') as text_file:
        termcolor.info('Creating hosts file')

        text_file.write('# This hosts file was generated by AdAway.py (https://github.com/edieguez/adaway-py)\n')
        text_file.write('# Do not modify it directly, it will be overwritten when AdAway.py is applied again.\n')
        text_file.write('127.0.0.1 %s\n' % gethostname())
        text_file.write('127.0.0.1 %s\n' % 'localhost')
        text_file.write('::1       %s\n' % 'localhost')

        blacklist = config.read('blacklist')
        custom_hosts = config.read('custom_hosts')
        whitelist = config.read('whitelist')
        whitelist.append('localhost')

        if custom_hosts:
            text_file.write('\n# Custom hosts\n')
            custom_hosts = sorted(custom_hosts.items(), key=operator.itemgetter(1))

            for host, ip in custom_hosts:
                text_file.write('%s\t%s\n' % (ip, host))

        if not deactivate:
            if blacklist:
                text_file.write('\n# Blacklisted hosts\n')

                for host in blacklist:
                    text_file.write('%s\t%s\n' % ('0.0.0.0', host))

            with sqlite3.connect(config.DATABASE) as connection:
                cursor = connection.cursor()

                text_file.write('\n# Blocked domains\n')

                hosts = cursor.execute('SELECT hostname FROM blacklist')
                hosts = set([host[0] for host in hosts])
                hosts = sorted(hosts.difference(whitelist))

                for host in hosts:
                    try:
                        text_file.write('%s\t%s\n' % ('0.0.0.0', host))
                    except UnicodeEncodeError as ex:
                        termcolor.error(str(ex))
        else:
            termcolor.info('Host blocking deactivated')
