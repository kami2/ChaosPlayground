from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from helpers.config_helper import ConfigHelper
import logging


class GoogleHelper:

    def __init__(self, credentials=None):
        self.config = ConfigHelper()
        self.auth = None

        if credentials is None:
            self.auth = self.auth_service_account()

    def auth_service_account(self):
        """
        Google Drive service with a service account.
        note: for the service account to work, you need to share the folder or
        files with the service account email.

        :return: google auth
        """

        settings = {
                    "client_config_backend": "service",
                    "service_config": {
                        "client_json_file_path": self.config.get_config("GOOGLE_SERVICE_ACCOUNT"),
                    }
                }
        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()
        return gauth

    def upload_file(self, filepath: str, dir_id: str = None):
        if dir_id is None:
            dir_id = self.config.get_config("GOOGLE_DRIVE_AI_IMAGES_DIRECTORY")
        try:
            drive = GoogleDrive(self.auth_service_account())
            file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": dir_id}]})
            file.SetContentFile(filepath)
            file.Upload()
            logging.info(f"Uploaded file {file['title']} to google drive directory {dir_id}")
            return file['title']
        except Exception as e:
            logging.info(f"Error {e}")


if __name__ == '__main__':
    gdrive = GoogleHelper()
    gdrive.upload_file("./test_files/test_file.jpg")
