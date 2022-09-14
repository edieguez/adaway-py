#! /usr/bin/env python
"""A python3 script to block publicity."""

from lib import util

if __name__ == '__main__':
    args = util.parse_arguments()

    util.create_configuration()
    util.create_database()
    util.populate_database()
    util.export_hosts_file(args.filename)
