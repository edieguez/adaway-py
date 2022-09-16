import os
import sqlite3
from sqlite3 import Cursor


class Database:
    def __init__(self, filename):
        self.filename = filename

    def database_exists(self):
        """Returns True if the file exists, otherwise returns False"""
        return os.path.exists(self.filename)

    def create_default_database(self):
        """Create a new database"""

        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()

            sql = (
                'CREATE TABLE blacklist ('
                '    hostname TEXT NOT NULL UNIQUE'
                ');'
            )

            cursor.execute(sql)

    def populate_database(self, hosts):
        """Populate the database using hosts files as source."""
        if hosts:
            with sqlite3.connect(self.filename) as connection:
                cursor = connection.cursor()

                for host in hosts:
                    try:
                        cursor.execute('INSERT INTO blacklist VALUES(?)', (host,))
                    except sqlite3.IntegrityError:
                        pass

    def get_blocked_hosts(self, whitelist: list) -> Cursor:
        whitelist.append('localhost')

        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()

            return cursor.execute(
                f'''SELECT hostname FROM blacklist
                WHERE hostname NOT IN ({','.join(['?'] * len(whitelist))})
                ORDER BY hostname''', whitelist
            )
