"""Download a file from internet."""

import re
import socket
import sys

try:
    # Python3
    from urllib import request
    from urllib.error import URLError
except ImportError:
    # Python2
    import urllib2 as request
    from urllib2 import URLError

from lib.termcolor import Termcolor, Font

termcolor = Termcolor()


def download_file(file_):
    """Download a file from internet and save it into a list.

    Keyword arguments:
    file_ --- the file that will be downloaded
    """
    termcolor.write('[!] Downloading source file: %s' % file_, Font.GREEN)

    try:
        data = request.urlopen(file_, timeout=3).read()
        data = data.decode('utf-8').split('\n')
    except socket.timeout:
        termcolor.write('[!] Timeout, aborting', Font.YELLOW)
        return list()
    except URLError as ex:
        termcolor.write('[!] ' + str(ex), Font.RED)
        return list()

    regex = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3} [^\s]+')
    domains = list()

    for domain in data:
        if domain and regex.match(domain):
            domains.append(domain.split()[1])

    return domains
