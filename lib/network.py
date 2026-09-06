"""Download a file from internet."""

import re
from urllib import request

from lib.termcolor import Termcolor

termcolor = Termcolor()

# Some sources answer 403 to the default urllib agent
USER_AGENT = 'adaway-py (+https://github.com/edieguez/adaway-py)'


def download_file(file_):
    """Download a file from internet and save it into a list.

    Keyword arguments:
    file_ --- the file that will be downloaded
    """
    termcolor.info(f'Downloading source file: {file_}')

    try:
        source = request.Request(file_, headers={'User-Agent': USER_AGENT})
        data = request.urlopen(source, timeout=30).read()
        data = data.decode('utf-8').split('\n')
    except OSError as ex:
        # URLError, timeouts and SSL failures are all OSError subclasses. One
        # unreachable source must not abort the remaining ones
        termcolor.error(f'{file_} - {str(ex)}')
        return list()

    # Separator is \s+ because some sources align entries with tabs
    regex = re.compile('^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\s+[^\\s]+')
    domains = list()

    for domain in data:
        if domain and regex.match(domain):
            domains.append(domain.split()[1])

    return domains
