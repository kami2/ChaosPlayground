from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from helpers.config_helper import ConfigHelper
import logging


class GoogleHelper:

    def __init__(self):
        self.config = ConfigHelper()
        self.auth = self.auth_service_account()
        self.drive = GoogleDrive(self.auth_service_account())

    def auth_service_account(self):
        """
        Google Drive service with a service account.
        note: for the service account to work, you need to share the folder or
        files with the service account email.

        :return: google auth
        """
        client_json_dict = {
                    "type": "service_account",
                    "project_id": self.config.get_config("GOOGLE_PROJECT_ID"),
                    "client_id": self.config.get_config("GOOGLE_CLIENT_ID"),
                    "client_email": self.config.get_config("GOOGLE_CLIENT_EMAIL"),
                    "client_x509_cert_url": self.config.get_config("GOOGLE_CLIENT_CERT_URL"),
                    "private_key_id": self.config.get_config("GOOGLE_PRIVATE_KEY_ID"),
                    "private_key": self.config.get_config("GOOGLE_PRIVATE_KEY")
                }
        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_dict": client_json_dict
            }
        }
        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()
        return gauth

    def upload_file(self, filepath: str, dir_id: str = None):
        if dir_id is None:
            dir_id = self.config.get_config("GOOGLE_DRIVE_AI_IMAGES_DIRECTORY")
        try:
            file = self.drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": dir_id}]})
            file.SetContentFile(filepath)
            file.Upload()
            logging.info(f"Uploaded file {file['title']} to google drive directory {dir_id}")
            return file['title']
        except Exception as e:
            logging.info(f"Error {e}")

    def is_file_exist(self, file_name: str):
        logging.info(f"Looking for {file_name}")
        search_file = self.drive.ListFile({'q': f"title='{file_name}'"}).GetList()
        if search_file:
            return True
        else:
            return False

    def list_image_files(self):
        directory = self.config.get_config('GOOGLE_DRIVE_AI_IMAGES_DIRECTORY')
        logging.info(f"List all files in {directory}")
        file_list = self.drive.ListFile({'q': f"'{directory}' in parents and trashed=false"}).GetList()
        jpg_files = [file for file in file_list if file['title'].lower().endswith('.jpg')]
        return jpg_files


if __name__ == '__main__':
    gdrive = GoogleHelper()
    # gdrive.upload_file("./test_files/test_file.jpg")
    # print(gdrive.is_file_exist("test_file.jpg"))
    print(gdrive.list_image_files())
