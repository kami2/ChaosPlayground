import logging
from flask import Flask, render_template, request
from generators.SickCreationsAutomation import post_image, create_image, index_files
from helpers.request_helper import api_required
from helpers.database_helper import DatabaseHelper

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

db = DatabaseHelper()


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


@app.route("/post_image", methods=['GET'])
@api_required
def schedule_post_image():
    db.add_event(event_name="post_image", results=post_image())
    return "Image posted"


@app.route("/create_image", methods=['GET'])
@api_required
def schedule_create_image():
    db.add_event(event_name="create_image", results=create_image())
    return "Image created"


@app.route("/index_file", methods=['GET'])
@api_required
def index_file():
    db.add_event(event_name="index_file", results=index_files())
    return "Database updated"


@app.route("/event_store", methods=['GET'])
def event_store():
    results = render_template("events.html", events=db.get_events_list())
    return results


@app.route("/add_event", methods=['POST'])
@api_required
def add_event():
    db.add_event(event_name="Remote event", results=request.get_json())
    return "Event Added"


@app.route("/upload_to_gdrive", methods=['POST'])
@api_required
def upload_to_gdrive():
    db.add_event(event_name="Upload file", results=request.get_json())
    return "File uploaded to gdrive"


if __name__ == '__main__':
    app.run()
