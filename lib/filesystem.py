"""Manage the Adaway database."""

import operator
from socket import gethostname

from lib.config import Config
from lib.termcolor import Termcolor

config = Config()
termcolor = Termcolor()


def export_hosts_headers(filename):
    """
    Keyword arguments:
    filename -- The file where the database will be exported
    """
    filename = filename or config.filename

    with open(filename, 'w') as hosts_file:
        termcolor.info('Creating hosts file')

        hosts_file.write('# This hosts file was generated by AdAway.py (https://github.com/edieguez/adaway-py)\n')
        hosts_file.write('# Do not modify it directly, it will be overwritten when AdAway.py is applied again.\n')
        hosts_file.write(f'127.0.0.1 {gethostname()}\n')
        hosts_file.write('127.0.0.1 %s\n' % 'localhost')
        hosts_file.write('::1       %s\n' % 'localhost')

        custom_hosts = config.read_key('custom_hosts')

        if custom_hosts:
            hosts_file.write('\n# Custom hosts\n')
            custom_hosts = sorted(custom_hosts.items(), key=operator.itemgetter(1))

            for host, ip in custom_hosts:
                hosts_file.write(f'{ip}\t{host}\n')


def export_hosts_file(filename, blocked_hosts, blacklisted_hosts):
    """Export the database to a text file.

    Keyword arguments:
    filename -- The file where the database will be exported
    """
    export_hosts_headers(filename)

    with open(filename, 'a') as hosts_file:
        if blacklisted_hosts:
            hosts_file.write('\n# Blacklisted hosts\n')

            for host in blacklisted_hosts:
                hosts_file.write('%s\t%s\n' % ('0.0.0.0', host))

        if blocked_hosts:
            hosts_file.write('\n')

            for host in blocked_hosts:
                try:
                    hosts_file.write(f'0.0.0.0\t{host[0]}\n')
                except UnicodeEncodeError as ex:
                    termcolor.error(str(ex))
