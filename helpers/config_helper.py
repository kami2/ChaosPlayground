import configparser

DEFAULT_CONFIG = "../config.ini"


class ConfigHelper:

    def __init__(self, config_file: str = None):
        if config_file is None:
            config_file = DEFAULT_CONFIG

        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_config(self, config_group: str, key: str):
        return self.config[config_group][key]
