import os
import json

class configurationClass(object):
    config = {}
    def __init__(self, config_file = None):
        self.config_file = config_file
        if self.config_file is None:
            self.config_file = 'config.json'

    def config_exists(self):
        return os.path.isfile(self.config_file)

    def get_config(self):
        config_data = None
        if self.config_exists() :
            with open(self.config_file) as json_file:
                config_data = json.load(json_file)
        return config_data

    def update_config(self, config_data):
        json_data = json.dumps(config_data, indent = 4)
        try:
            with open(self.config_file, 'w') as fh:
                fh.write(json_data)
        except IOError as err:
            return (500, 'Internal Error: {0}'.format(err.strerror))