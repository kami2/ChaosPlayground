import logging
from helpers.google_helper import GoogleHelper
from helpers.database_helper import DatabaseHelper
import requests


def post_image():
    return "Posting image process"


def create_image():
    return "Creating image process"


def index_files():
    logging.info("Indexing files in database")
    updated = 0
    try:
        gdrive = GoogleHelper()
        db = DatabaseHelper()
        files = gdrive.list_image_files()
        for file in files:
            if not db.is_img_exist(file['title']):
                insert_to_db = db.insert_img_data(img_id=file['id'],
                                                  image_name=file['title'],
                                                  is_deleted=False,
                                                  is_published=False,
                                                  )

    except Exception as e:
        logging.error(f"ERROR: {e}")


if __name__ == '__main__':
    index_files()
