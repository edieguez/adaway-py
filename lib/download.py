import re
from urllib import request


def download_file(wpath):
    data = request.urlopen(wpath).read()
    data = data.decode('utf-8').split('\n')

    regex = re.compile('^\d')
    domains = list()

    print("downloading:", wpath)

    for domain in data:
        if domain and regex.match(domain):
            domains.append(domain.split()[1])

    return domains
