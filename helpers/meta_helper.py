from helpers.config_helper import ConfigHelper
import requests


class InstaHelper:
    def __init__(self):

        self.user_id = None
        self.config = ConfigHelper()
        self.client_secret = self.config.get_config("INSTAGRAM_APP_SECRET")
        self.client_id = self.config.get_config("INSTAGRAM_APP_ID")
        self.access_token = self.config.get_config("INSTAGRAM_ACCESS_TOKEN")

        self.url = f"https://graph.facebook.com/v18.0/{self.config.get_config('INSTAGRAM_ACCOUNT_ID')}"

    # probably I do not need this, will find out tomorrow
    def get_token(self):
        params = {"grant_type": "fb_exchange_token",
                  "client_id": self.client_id,
                  "client_secret": self.client_secret,
                  "fb_exchange_token": self.access_token}
        response = requests.get("https://graph.facebook.com/v18.0/oauth/access_token", params=params)
        return response.json()

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
    meta = InstaHelper()
    image = "https://cdn.leonardo.ai/users/e3428632-6606-4fcd-a690-a32e0f9437d1/generations/51f24f72-3511-423f-8238-0c3ce205a88a/Isometric_Scifi_Buildings_Step_into_a_world_of_vibrant_colors_0.jpg"
    print(meta.post_image_on_instagram(image, "Caption here #whatamdoinghere"))
    # print(meta.get_token())

