import sqlalchemy as db
import logging
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")


class DatabaseHelper:

    def __init__(self):
        self._engine = db.create_engine(f'mysql+pymysql://{config["DATABASE_CONNECTION"]["Login"]}:'
                                        f'{config["DATABASE_CONNECTION"]["Password"]}@'
                                        f'{config["DATABASE_CONNECTION"]["Host"]}/'
                                        f'{config["DATABASE_CONNECTION"]["DatabaseName"]}')
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
    logging.basicConfig(level=logging.DEBUG)
    connect = DatabaseHelper()
    connect.test_connection()
