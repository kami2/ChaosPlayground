import logging
from helpers.google_helper import GoogleHelper
from helpers.database_helper import DatabaseHelper
from helpers.meta_helper import InstaHelper


def post_image():
    logging.info("Posting image process")
    try:
        logging.info("Initializing GoogleHelper")
        gdrive = GoogleHelper()
        logging.info("Initializing DatabaseHelper")
        db = DatabaseHelper()
        logging.info("Initializing InstaHelper")
        meta = InstaHelper()
        while True:
            latest_file = db.get_the_latest_file()
            if len(latest_file) > 0:
                if not gdrive.is_file_exist(latest_file[0]['imageName']):
                    db.set_deleted(latest_file[0]['id'])
                    continue
                else:
                    logging.info(f"Post image {latest_file[0]['imageName']}")
                    caption = "#ai #isometric #gamedesign #automation"
                    if latest_file[0]['prompt']:
                        caption = latest_file[0]['prompt'].split(".", 1)[0]
                    image = meta.post_image_on_instagram(image_url=latest_file[0]['url'], caption=caption)
                    if image.status_code == 200:
                        db.set_published(latest_file[0]['id'])
                        return {'Status': image.status_code, "Instagram post id": image.json()['id']}
            else:
                logging.info("There is no image to publish")
                break

    except Exception as e:
        logging.info(f"ERROR: {e}")


def process_generated_image(payload: dict):
    logging.info("Processing image")
    try:
        logging.info("Initializing GoogleHelper")
        gdrive = GoogleHelper()
        logging.info("Initializing DatabaseHelper")
        db = DatabaseHelper()
        file_id, file_title, file_url = gdrive.upload_file(payload['file_url'])
        db.insert_img_data(img_id=file_id,
                           image_name=file_title,
                           is_deleted=False,
                           is_published=False,
                           created_date=payload["created_at"],
                           url=file_url,
                           published_date='',
                           prompts=payload['prompt'])
        db.add_event("process_generated_image", results=f"processed {file_id} | {file_title}")
    except Exception as e:
        logging.info(f"ERROR: {e}")
    return {"Image processed"}


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
                                   url=file['webContentLink'],
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
