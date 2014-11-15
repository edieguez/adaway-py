<<<<<<< HEAD
import sqlite3
from os.path import exists

=======
import operator
import sqlite3
from os.path import exists

from .config import read_config
from .download import download_file

>>>>>>> dev

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

<<<<<<< HEAD
def insert_blacklisted_domains(database, blacklist, whitelist=None):
=======
def insert_blacklisted_domains(database, config):
>>>>>>> dev
    if not exists(database):
        create_database(database)

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
<<<<<<< HEAD

        for domain in blacklist:
            if domain in whitelist:
                continue

            try:
                cursor.execute('INSERT INTO blacklist VALUES(NULL, ?)', (domain,))
            except sqlite3.IntegrityError:
                pass

def export_database(database, filename):
=======
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
>>>>>>> dev
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()

        with open(filename, 'w') as text_file:
<<<<<<< HEAD
=======
            custom_hosts = read_config(config, 'custom_hosts')
            custom_hosts = sorted(custom_hosts.items(), key=operator.itemgetter(1))

            for host, ip in custom_hosts:
                text_file.write('%s\t%s\n' % (ip, host))

            text_file.write('\n')

>>>>>>> dev
            hosts = cursor.execute('SELECT hostname FROM blacklist ORDER BY hostname')
            hosts = [host[0] for host in hosts]

            for host in hosts:
<<<<<<< HEAD
                text_file.write('%s    %s\n' % ('0.0.0.0', host))
=======
                text_file.write('%s\t%s\n' % ('0.0.0.0', host))
>>>>>>> dev
