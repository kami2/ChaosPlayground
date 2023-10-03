import logging
from helpers.google_helper import GoogleHelper
from helpers.database_helper import DatabaseHelper


def post_image():
    logging.info("Posting image process...")
    # TODO :
    #  1. Find info in database about the oldest not published and not deleted image
    #  2. Check if that file exist on gdrive, if not set isDeleted to true
    #  3. Post image to instagram and set isPublished and update published date
    return "Posted images: not implemented yet"


def create_image():
    return "Created images: not implemented yet"


def index_files():
    logging.info("Indexing files in database")
    image_list = []
    updated = 0
    skipped = 0
    try:
        logging.info("Initializing GoogleHelper")
        gdrive = GoogleHelper()
        logging.info("Initializing DatabaseHelper")
        db = DatabaseHelper()
        files = gdrive.list_image_files()
        for file in files:
            if not db.is_img_exist(file['id']):
                db.insert_img_data(img_id=file['id'],
                                   image_name=file['title'],
                                   is_deleted=False,
                                   is_published=False,
                                   created_date=file["createdDate"],
                                   url=file['downloadUrl'],
                                   published_date='',
                                   prompts='')
                image_list.append(file['title'])
                logging.info(f"Image {file['title']} index added to database")
                updated += 1
            else:
                logging.info(f"File already in db, skipping {file['title']}")
                skipped += 1
        return f"Updated: {updated}, Skipped: {skipped}, Indexed files: {image_list}"

    except Exception as e:
        logging.error(f"ERROR: {e}")


if __name__ == '__main__':
    index_files()
