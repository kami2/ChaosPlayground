import functools
from flask import request
from helpers.config_helper import ConfigHelper

config = ConfigHelper()


def is_valid(api_key):
    if api_key == config.get_config("CRON_SECRET"):
        return True


def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        if authorization_header is None or not authorization_header.startswith("Bearer "):
            return {"message": "Invalid or missing Authorization header"}, 401

        api_key = authorization_header.split(" ")[1]

        if is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return {"message": "The provided access token is not valid"}, 403

    return decorator
