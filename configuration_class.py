import os
import json

class configurationClass(object):
    config = {}
    def __init__(self, config_file = None, root_path = None ):
        if root_path is None:
            root_path = '.'
        if config_file is None:
            config_file = 'config.json'
        self.config_file = root_path +'/'+ config_file

    def config_exists(self):
        return os.path.isfile(self.config_file)

    def get_config(self,):
        config_data = None
        print("FILE {}".format(self.config_file))
        if self.config_exists() :
            with open(self.config_file) as json_file:
                config_data = json.load(json_file)
                print("FILE {}".format(self.config_file))
        return config_data

    def update_config(self, config_data):
        json_data = json.dumps(config_data, indent = 4)
        try:
            with open(self.config_file, 'w') as fh:
                fh.write(json_data)
        except IOError as err:
            return (500, 'Internal Error: {0}'.format(err.strerror))