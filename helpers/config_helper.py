import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
DEFAULT_CONFIG = "../.env"


class ConfigHelper:

    def __init__(self, config_file: str = None):
        self.config = load_dotenv(DEFAULT_CONFIG)
        if config_file is not None:
            logging.info(f"Get config from: {config_file}")
            self.config = load_dotenv(config_file)

    def get_config(self, key: str):
        if self.config:
            logging.info(f"Get variable {key} from config path: {DEFAULT_CONFIG}")
            return os.environ.get(key)
        else:
            logging.info(f"Get environment variable {key}")
            return os.environ.get(key)
