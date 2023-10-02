import functools
from flask import request
from helpers.config_helper import ConfigHelper

config = ConfigHelper()


def is_valid(api_key):
    if api_key == config.get_config("API_KEY"):
        return True


def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers and "api_key" in request.headers:
            api_key = request.headers.get("api_key")
        elif request.args.get("api_key"):
            api_key = request.args.get("api_key")
        else:
            return {"message": "Please provide an API key"}, 400
        if is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403
    return decorator
