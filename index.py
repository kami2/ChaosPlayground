import logging
from flask import Flask, render_template, request
from apps.test_import import TestImport
from helpers.database_helper import DatabaseHelper
from apps.ImageGenerator import ImageGenerator
from helpers.request_helper import api_required

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

PAYLOAD_CACHE = {}


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


@app.route("/payload_cache", methods=['GET'])
def payload_cache():
    return PAYLOAD_CACHE


@app.route("/webhook", methods=['POST'])
def webhook():
    payload = request.get_json()
    raw = request.data
    PAYLOAD_CACHE['WEBHOOK'] = payload
    PAYLOAD_CACHE['RAW_WEBHOOK'] = raw
    return "Got payload"


@app.route("/hello", methods=['POST'])
@api_required
def hello():
    try:
        if "name" in request.json and request.json['name']:
            return f"Hello {request.json['name']}"
        else:
            return "Please provide your name"
    except Exception as e:
        return f"ERROR: {e}"


@app.route("/test")
def test_area():
    TestImport("Did i make mistake?")
    try:
        conn = DatabaseHelper()
        conn.test_connection()
        msg = "Success"
    except Exception as e:
        return f"ERROR: {e}"

    return msg


@app.route("/create-image", methods=['POST'])
def create_image():
    try:
        prompt = request.json['prompt']
        image = ImageGenerator(prompt)
        image_url = image.get_image_url()
        response = {"image_url": image_url}
        logging.info(response)
    except Exception as e:
        return f"ERROR: {e}"

    return response


if __name__ == '__main__':
    app.run()
