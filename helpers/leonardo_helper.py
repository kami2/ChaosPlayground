import requests
from helpers.config_helper import ConfigHelper


class LeonardoHelper:
    def __init__(self):
        self.config = ConfigHelper()
        self.headers = self.get_headers()

    def get_headers(self):
        return {"Authorization": f"Bearer {self.config.get_config('LEONARDO_ACCESS_TOKEN')}"}

    def get_prompt(self):
        # Prompt generator? Not sure if I want use leonardo prompt generator or chatgpt
        pass

    def generate_image(self, prompt: str):
        # Build params and send request
        params = {
            "prompt": prompt
        }
        response = requests.get("url", params=params, headers=self.get_headers())
        return {"Status": response.status_code}

    def check_status(self):
        # maybe I should check if image is ready or still processing
        pass
