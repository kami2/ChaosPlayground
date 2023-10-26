import os
from dotenv import load_dotenv
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_NAME = ".env"
DEFAULT_CONFIG = fr"{ROOT_DIR}\{CONFIG_NAME}"


class ConfigHelper:

    def __init__(self, config_file: str = None):
        self.config = load_dotenv(DEFAULT_CONFIG)
        self.config_file = config_file

        if self.config_file is not None:
            logging.info(f"Get config from: {self.config_file}")
            self.config = load_dotenv(self.config_file)

    def get_config(self, key: str):
        if self.config_file:
            logging.info(f"Get variable {key} from config: {CONFIG_NAME}")
        else:
            logging.info(f"Get environment variable {key}")
        return os.environ.get(key)

    @staticmethod
    def get_cache_dir():
        if not os.path.exists("cache"):
            os.makedirs("cache")

        return "cache"
