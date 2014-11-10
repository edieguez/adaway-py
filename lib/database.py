import sqlite3
from os.path import exists


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

def insert_blacklisted_domains(database, blacklist, whitelist=None):
    if not exists(database):
        create_database(database)

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()

        for domain in blacklist:
            if domain in whitelist:
                continue

            try:
                cursor.execute('INSERT INTO blacklist VALUES(NULL, ?)', (domain,))
            except sqlite3.IntegrityError:
                pass
