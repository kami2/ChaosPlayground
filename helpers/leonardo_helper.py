import requests
from helpers.config_helper import ConfigHelper


class LeonardoHelper:
    def __init__(self):
        self.config = ConfigHelper()
        self.headers = self.get_headers()

    def get_headers(self):
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.config.get_config('LEONARDO_ACCESS_TOKEN')}"
        }

    def get_prompt(self):
        # Prompt generator? Not sure if I want use leonardo prompt generator or chatgpt
        pass

    def generate_image(self, prompt: str):
        # https://docs.leonardo.ai/reference/creategeneration
        generation_id = None
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        payload = {
            "height": 768,
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
            "prompt": prompt,
            "num_images": 1,
            "width": 512,
            "alchemy": True,
            "nsfw": False
        }
        response = requests.post(url=url, json=payload, headers=self.get_headers())
        if response.status_code == 200:
            generation_id = response.json()['sdGenerationJob']['generationId']
        return generation_id

    def get_generation(self, generation_id: str):
        # https://docs.leonardo.ai/reference/getgenerationbyid
        url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
        response = requests.get(url=url, headers=self.get_headers())
        # TODO need to do extra stuff here
        return {"Status": response.status_code}
