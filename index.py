import logging
from flask import Flask, render_template
from datetime import datetime
from generators.SickCreationsAutomation import post_image, create_image

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

PAYLOAD_CACHE = {}


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


@app.route("/post_image", methods=['GET'])
def schedule_post_image():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    PAYLOAD_CACHE[date_time] = post_image()
    return "Image posted"


@app.route("/create_image", methods=['GET'])
def schedule_create_image():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    PAYLOAD_CACHE[date_time] = create_image()
    return "Image created"


@app.route("/payload_cache", methods=['GET'])
def payload_cache():
    return PAYLOAD_CACHE


if __name__ == '__main__':
    app.run()
