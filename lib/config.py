import json

def read_config(config_file):
    ad_files = list()
    white_list = list()

    with open(config_file) as raw_config:
        json_file = json.load(raw_config)
        ad_files = json_file['ad_files']
        white_list = json_file['white_list']

    return ad_files, white_list
