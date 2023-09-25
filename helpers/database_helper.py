import sqlalchemy as db
import logging
from helpers.config_helper import ConfigHelper

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
            if not self.is_table_exist("creations"):
                logging.info("Creating table...")
                self._conn.execute("CREATE TABLE creations "
                                   "(id BIGINT,"
                                   "image_name VARCHAR(255),"
                                   "isDeleted BOOLEAN,"
                                   "isPublished BOOLEAN,"
                                   "createdDate DATETIME,"
                                   "url VARCHAR(600),"
                                   "publishedDate DATETIME,"
                                   "prompt VARCHAR(1000),"
                                   "PRIMARY KEY (id, image_name));")
            else:
                logging.info("Table already exist")
        except Exception as e:
            logging.error("Cannot connect to db")
            raise e

    def is_table_exist(self, table_name: str) -> bool:
        if db.inspect(self._engine).has_table(table_name):
            return True
        else:
            return False

    def execute_query(self, query: str, **kwargs):
        try:
            self._conn.execute(query, **kwargs)
        except Exception as e:
            logging.error(f"Cannot execute query: {e}")

    def insert_img_data(self, img_id, image_name, is_deleted, is_published, date, url, published_date, prompts):
        sql_insert = """
                     INSERT INTO creations (id, image_name, isDeleted, isPublished, date, url, publishedDate, prompts)
                     VALUES (:id, :image_name, :isDeleted, :isPublished, :date, :url, :publishedDate, :prompts)
                     """
        self.execute_query(sql_insert,
                           id=img_id,
                           image_name=image_name,
                           isDeleted=is_deleted,
                           isPublished=is_published,
                           date=date,
                           url=url,
                           publishedDate=published_date,
                           prompts=prompts)


if __name__ == '__main__':
    conn = DatabaseHelper()
    conn.is_table_exist("creations")
