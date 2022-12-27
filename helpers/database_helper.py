import sqlalchemy as db
import logging
from helpers.config_helper import ConfigHelper

logging.basicConfig(level=logging.DEBUG)
config = ConfigHelper()


class DatabaseHelper:

    def __init__(self):
        self._engine = db.create_engine(f'mysql+pymysql://{config.get_config("MYSQL_DB_LOGIN")}:'
                                        f'{config.get_config("MYSQL_DB_PASSWORD")}@'
                                        f'{config.get_config("MYSQL_DB_HOST")}/'
                                        f'{config.get_config("MYSQL_DB_NAME")}')
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
