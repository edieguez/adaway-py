import os
import sqlite3
from contextlib import closing


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

    def clear(self):
        """Remove every hostname so a full refresh drops upstream deletions."""
        with sqlite3.connect(self.filename) as connection:
            connection.execute('DELETE FROM blacklist')

    def populate_database(self, hosts):
        """Populate the database using hosts files as source."""
        if hosts:
            with sqlite3.connect(self.filename) as connection:
                connection.executemany(
                    'INSERT OR IGNORE INTO blacklist VALUES(?)', ((host,) for host in hosts)
                )

    def get_blocked_hosts(self, whitelist: list) -> list:
        exempt = tuple(set(whitelist) | {'localhost'})

        with closing(sqlite3.connect(self.filename)) as connection:
            rows = connection.execute('SELECT hostname FROM blacklist ORDER BY hostname').fetchall()

        return [host for (host,) in rows if not _is_exempt(host, exempt)]


def _is_exempt(hostname: str, exempt: tuple) -> bool:
    """A whitelisted domain also covers every one of its subdomains."""
    return any(hostname == domain or hostname.endswith(f'.{domain}') for domain in exempt)
