import operator
import sqlite3
from os.path import exists
from socket import gethostname

from .config import read_config
from .download import download_file


def create_database(filename):
    with sqlite3.connect(filename) as connection:
        cursor = connection.cursor()
        sql = (
            'CREATE TABLE blacklist ('
            '    id INTEGER NOT NULL PRIMARY KEY,'
            '    hostname TEXT NOT NULL UNIQUE'
            ');'
        )
        cursor.execute(sql)

def insert_blacklisted_domains(database, config):
    if not exists(database):
        create_database(database)

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        blacklist, whitelist = read_config(config, 'blacklist', 'whitelist')

        for file_ in blacklist:
            data = download_file(file_)

            for domain in data:
                if domain in whitelist:
                    continue

                try:
                    cursor.execute('INSERT INTO blacklist VALUES(NULL, ?)', (domain,))
                except sqlite3.IntegrityError:
                    pass

def export_database(database, config, filename='/etc/hosts'):
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()

        with open(filename, 'w') as text_file:
            custom_hosts = read_config(config, 'custom_hosts')
            custom_hosts = sorted(custom_hosts.items(), key=operator.itemgetter(1))
            custom_hosts.insert(0, [gethostname(), '127.0.0.1'])

            for host, ip in custom_hosts:
                text_file.write('%s\t%s\n' % (ip, host))

            text_file.write('\n')

            hosts = cursor.execute('SELECT hostname FROM blacklist ORDER BY hostname')
            hosts = [host[0] for host in hosts]

            for host in hosts:
                text_file.write('%s\t%s\n' % ('0.0.0.0', host))
