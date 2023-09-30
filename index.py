import logging
from flask import Flask, render_template
from datetime import datetime
from generators.SickCreationsAutomation import post_image, create_image, index_files

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
    date_time_now = now.strftime("%m/%d/%Y, %H:%M:%S")
    PAYLOAD_CACHE[date_time_now] = post_image()
    return "Image posted"


@app.route("/create_image", methods=['GET'])
def schedule_create_image():
    now = datetime.now()
    date_time_now = now.strftime("%m/%d/%Y, %H:%M:%S")
    PAYLOAD_CACHE[date_time_now] = create_image()
    return "Image created"


@app.route("/index_file", methods=['GET'])
def index_file():
    now = datetime.now()
    date_time_now = now.strftime("%m/%d/%Y, %H:%M:%S")
    PAYLOAD_CACHE[date_time_now] = index_files()
    return "Database updated"


@app.route("/payload_cache", methods=['GET'])
def payload_cache():
    return PAYLOAD_CACHE


if __name__ == '__main__':
    app.run()
