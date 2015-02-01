import re
import socket
from urllib import request

import lib.termcolor as termcolor


def download_file(file):
    termcolor.write('    [!] Downloading source file: %s' % file, termcolor.Font.GREEN)
    try:
        data = request.urlopen(file, timeout=3).read()
        data = data.decode('utf-8').split('\n')
    except socket.timeout:
        termcolor.write('    [!] Timeout, aborting', termcolor.Font.YELLOW)
        return list()

    regex = re.compile('^\d')
    domains = list()

    for domain in data:
        if domain and regex.match(domain):
            domains.append(domain.split()[1])

    return domains
