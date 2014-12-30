import re
import socket
from urllib import request


def download_file(wpath):
    try:
        data = request.urlopen(wpath, timeout=5).read()
        data = data.decode('utf-8').split('\n')
    except socket.timeout:
        return list()

    regex = re.compile('^\d')
    domains = list()

    for domain in data:
        if domain and regex.match(domain):
            domains.append(domain.split()[1])

    return domains
