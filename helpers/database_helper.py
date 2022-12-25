import sqlalchemy as db
import logging
import os
from helpers.config_helper import ConfigHelper

logging.basicConfig(level=logging.DEBUG)
config = ConfigHelper()


class DatabaseHelper:

    def __init__(self):
        self._engine = db.create_engine(f'mysql+pymysql://{os.environ.get("Login")}:'
                                        f'{os.environ.get("Password")}@'
                                        f'{os.environ.get("Host")}/'
                                        f'{os.environ.get("DatabaseName")}')
        self._conn = self._engine.connect()

    def test_connection(self):
        try:
            if not db.inspect(self._engine).has_table('Test'):
                logging.info("Creating table...")
                self._conn.execute("CREATE TABLE Test (Name varchar(255));")
            else:
                logging.info("Table already exist")
        except Exception as e:
            logging.error("Cannot connect to db")
            raise e


if __name__ == '__main__':
    conn = DatabaseHelper()
    conn.test_connection()
