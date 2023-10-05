from helpers.config_helper import ConfigHelper
import requests


class MetaHelper:
    def __init__(self, account_id: str):

        self.user_id = None
        self.config = ConfigHelper()
        self.access_token = None

        if account_id == "INSTAGRAM_ACCOUNT_ID":
            self.access_token = self.config.get_config("INSTAGRAM_ACCESS_TOKEN")

        self.url = f"https://graph.facebook.com/v18.0/{self.config.get_config(account_id)}"

    def upload_image(self, image_url: str, caption: str):
        params = {
            "access_token": self.access_token,
            "caption": caption,
            "image_url": image_url
        }
        response = requests.post(f"{self.url}/media", params=params)
        return response.json()["id"]

    def post_image_on_instagram(self, image_url: str, caption: str):
        params = {
            "access_token": self.access_token,
            "creation_id": self.upload_image(image_url=image_url, caption=caption)
        }
        response = requests.post(f"{self.url}/media_publish", params=params)
        return response


if __name__ == '__main__':
    meta = MetaHelper("INSTAGRAM_ACCOUNT_ID")
    image = "https://cdn.leonardo.ai/users/e3428632-6606-4fcd-a690-a32e0f9437d1/generations/51f24f72-3511-423f-8238-0c3ce205a88a/Isometric_Scifi_Buildings_Step_into_a_world_of_vibrant_colors_0.jpg"
    print(meta.post_image_on_instagram(image, "Caption here #whatamdoinghere"))

