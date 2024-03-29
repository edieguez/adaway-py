#! /usr/bin/env python
"""A python3 script to block publicity."""

from lib import util

if __name__ == '__main__':
    args = util.parse_arguments()

    if args.a:
        util.apply_host_blocking(args.hosts_file)
    elif args.d:
        util.deactivate_host_blocking(args.hosts_file)
    elif args.w:
        util.whitelist_hosts(args.hosts_file, args.w)
    elif args.W:
        util.remove_whitelisted_hosts(args.hosts_file, args.W)
    elif args.b:
        util.blacklist_hosts(args.hosts_file, args.b)
    elif args.B:
        util.remove_blacklisted_hosts(args.hosts_file, args.B)
    else:
        util.fully_apply_host_blocking(args.hosts_file)
