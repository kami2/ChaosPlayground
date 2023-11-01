import logging
from flask import Flask, render_template, request
from generators.SickCreationsAutomation import post_image, index_files, process_generated_image
from helpers.request_helper import api_required
from helpers.database_helper import DatabaseHelper
from helpers.google_helper import GoogleHelper

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
    post_image()
    return "Image posted"


@app.route("/index_file", methods=['GET'])
@api_required
def index_file():
    db.add_event(event_name="index_file", results=index_files())
    return "Database updated"


@app.route("/event_store", methods=['GET'])
def event_store():
    results = render_template("events.html", events=db.get_events_list())
    return results


@app.route("/process_generated_image", methods=['POST'])
@api_required
def worker_generated_image():
    try:
        payload = request.get_json()
        results = process_generated_image(payload)
        return f"Image processed: {results}"
    except Exception as e:
        return f"FAILED : {e}"


@app.route("/add_event", methods=['POST'])
@api_required
def add_event():
    db.add_event(event_name="Remote event", results=request.get_json())
    return "Event Added"


@app.route("/upload_to_gdrive", methods=['POST'])
@api_required
def upload_to_gdrive():
    payload = request.get_json()
    gdrive = GoogleHelper()
    uploaded_image = gdrive.upload_file(payload['file_url'])
    if uploaded_image:
        db.add_event(event_name="Upload file from url", results=payload)
    return f"File uploaded to gdrive {uploaded_image}"


if __name__ == '__main__':
    app.run()
