import os
from dotenv import load_dotenv
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_NAME = ".env"
DEFAULT_CONFIG = fr"{ROOT_DIR}\{CONFIG_NAME}"


class ConfigHelper:

    def __init__(self, config_file: str = None):
        self.config = load_dotenv(DEFAULT_CONFIG)
        if config_file is not None:
            logging.info(f"Get config from: {config_file}")
            self.config = load_dotenv(config_file)

    def get_config(self, key: str):
        if self.config:
            logging.info(f"Get variable {key} from config: {CONFIG_NAME}")
            return os.environ.get(key)
        else:
            logging.info(f"Get environment variable {key}")
            return os.environ.get(key)
