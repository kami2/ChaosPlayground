from helpers.config_helper import ConfigHelper
import openai

config = ConfigHelper()


class ImageGenerator:

    def __init__(self, prompt: str, size: str = "1024x1024"):
        self.client = openai
        self.client.api_key = config.get_config("OPEN_AI_APIKEY")
        self.image = self.create_image(prompt, size)

    def create_image(self, prompt: str, size: str = "1024x1024"):
        return self.client.Image.create(prompt=prompt, n=1, size=size)

    def get_image_url(self):
        return self.image['data'][0]['url']

    def create_image_variation(self, image: str, prompt: str, size: str = "1024x1024"):
        return self.client.Image.create_variation(prompt=prompt, n=1, size=size, image=open(image, "rb"))
