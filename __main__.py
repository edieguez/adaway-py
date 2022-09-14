#! /usr/bin/env python
"""A python3 script to block publicity."""

from lib import util

if __name__ == '__main__':
    args = util.parse_arguments()

    if args.a:
        util.apply_host_blocking(args.filename)
    elif args.d:
        util.deactivate_host_blocking(args.filename)
    elif args.w:
        util.whitelist_hosts(args.filename, args.w)
    elif args.b:
        util.blacklist_hosts(args.filename, args.b)
    else:
        util.fully_apply_host_blocking(args.filename)
