import openai
from helpers.config_helper import ConfigHelper


class OpenAiHelper:
    def __init__(self):
        self.config = ConfigHelper()
        self.client = openai
        self.client.api_key = self.config.get_config("OPEN_AI_APIKEY")

    def generate_prompt(self):
        prompt = self.client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[],
            temperature=0.6,
            max_tokens=256
        )
        return prompt
