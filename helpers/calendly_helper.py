import json

import requests
from helpers.config_helper import ConfigHelper

config = ConfigHelper()


def get_current_user():
    headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {config.get_config('CALENDLY_SECRET')}"
    }
    response = requests.get("https://api.calendly.com/users/me", headers=headers)

    return response.json()['resource']


def create_calendly_subscription():
    signing_key = config.get_config("CALENDLY_SIGNING_KEY")
    headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {config.get_config('CALENDLY_SECRET')}"
    }
    payload = {
        "url": "https://chaotic.vercel.app/webhook",
        "events": [
            "invitee.created",
            "invitee.canceled"
        ],
        "organization": get_current_user()['current_organization'],
        "scope": "organization",
        "signing_key": signing_key
    }
    response = requests.post("https://api.calendly.com/webhook_subscriptions", data=json.dumps(payload), headers=headers)
    return response


if __name__ == '__main__':
    create_calendly_subscription()

