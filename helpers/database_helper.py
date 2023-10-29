import sqlalchemy as db
import logging
from sqlalchemy.sql import text
from helpers.config_helper import ConfigHelper
from datetime import datetime

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
                logging.info("Creating table creations...")
                self._conn.execute("CREATE TABLE creations "
                                   "(id VARCHAR(255),"
                                   "imageName VARCHAR(255),"
                                   "isDeleted BOOLEAN,"
                                   "isPublished BOOLEAN,"
                                   "createdDate DATETIME,"
                                   "url VARCHAR(600),"
                                   "publishedDate DATETIME,"
                                   "prompt VARCHAR(1000),"
                                   "PRIMARY KEY (id));")
            elif not self.is_table_exist("events"):
                self._conn.execute("CREATE TABLE events "
                                   "(id INT AUTO_INCREMENT,"
                                   "date DATETIME,"
                                   "event_name VARCHAR(50),"
                                   "results VARCHAR(600),"
                                   "PRIMARY KEY (id));")
            else:
                logging.info("Tables already exist")
        except Exception as e:
            logging.error("Cannot connect to db")
            raise e

    def get_events_list(self):
        sql_select = "SELECT * FROM events ORDER BY date DESC LIMIT 100"
        results = self.execute_query(sql_select)
        if results.rowcount >= 1:
            return results.fetchall()
        else:
            return []

    def add_event(self, event_name, results):
        sql_insert = """
                     INSERT INTO events (date, event_name, results)
                     VALUES (:date, :event_name, :results)
                     """
        self.execute_query(sql_insert, date=datetime.now(), event_name=str(event_name), results=str(results))

    def is_table_exist(self, table_name: str) -> bool:
        if db.inspect(self._engine).has_table(table_name):
            return True
        else:
            return False

    def execute_query(self, query: str, **kwargs):
        try:
            query_text = text(query)
            return self._conn.execute(query_text, **kwargs)
        except Exception as e:
            logging.error(f"Cannot execute query: {e}")

    def insert_img_data(self, img_id, image_name, is_deleted, is_published, created_date, url, published_date, prompts):
        sql_insert = """
                     INSERT INTO creations (id, imageName, isDeleted, isPublished, createdDate, url, publishedDate, prompt)
                     VALUES (:id, :imageName, :isDeleted, :isPublished, :createdDate, :url, :publishedDate, :prompt)
                     """
        self.execute_query(sql_insert,
                           id=img_id,
                           imageName=image_name,
                           isDeleted=is_deleted,
                           isPublished=is_published,
                           createdDate=created_date,
                           url=url,
                           publishedDate=published_date,
                           prompt=prompts)

    def is_img_exist(self, file_id: str):
        query = f"SELECT id FROM creations WHERE id = '{file_id}'"
        row_count = self.execute_query(query)
        if row_count.rowcount >= 1:
            return True
        else:
            return False

    def get_the_latest_file(self):
        query = "SELECT * FROM creations WHERE isPublished IS FALSE AND isDeleted IS FALSE ORDER BY createdDate ASC LIMIT 1"
        return self.execute_query(query).fetchall()

    def set_deleted(self, image_id: str):
        query = f"UPDATE creations SET isDeleted = TRUE WHERE id = '{image_id}'"
        return self.execute_query(query)

    def set_published(self, image_id: str):
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"UPDATE creations SET isPublished = TRUE, publishedDate = '{current_date}' WHERE id = '{image_id}'"
        return self.execute_query(query)


if __name__ == '__main__':
    conn = DatabaseHelper()
    # conn.test_connection()
    # print(conn.get_the_latest_file())
    conn.set_published("1a1AlhQbvmvFd6iEwPIgoq-i42d6pLp2q")
