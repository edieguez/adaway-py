"""Download a file from internet."""

import re
import socket
import sys
from urllib import request
from urllib.error import URLError

import lib.termcolor as termcolor


def download_file(file_):
    """Download a file from internet and save it into a list.

    Keyword arguments:
    file_ --- the file that will be downloaded
    """
    termcolor.write('    [!] Downloading source file: %s' % file_, termcolor.Font.GREEN)
    try:
        data = request.urlopen(file_, timeout=3).read()
        data = data.decode('utf-8').split('\n')
    except socket.timeout:
        termcolor.write('    [!] Timeout, aborting', termcolor.Font.YELLOW)
        return list()
    except URLError:
        termcolor.write('    [!] Network error: You don\'t have an internet connection', termcolor.Font.RED)
        sys.exit(2)

    regex = re.compile('^\d')
    domains = list()

    for domain in data:
        if domain and regex.match(domain):
            domains.append(domain.split()[1])

    return domains
