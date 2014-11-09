import json
from os.path import exists

def read_config(config_file):
    if not exists(config_file):
        write_default_config(config_file)

    ad_files = list()
    whitelist = list()

    with open(config_file) as raw_config:
        json_file = json.load(raw_config)
        ad_files = json_file['ad_files']
        whitelist = json_file['whitelist']

    return ad_files, whitelist

def write_default_config(filename):
    with open(filename, 'w') as config_file:
        raw_config = (
            '{\n'
            '    "ad_files": [\n'
            '        "domain_1.com",\n'
            '        "domain_2.com",\n'
            '        "domain_3.com",\n'
            '        "domain_4.com",\n'
            '        "domain_5.com"\n'
            '    ],\n'
            '    "whitelist": [\n'
            '        "white_1.com",\n'
            '        "white_2.com",\n'
            '        "white_3.com"\n'
            '    ]\n'
            '}'
        )

        config_file.write(raw_config)
