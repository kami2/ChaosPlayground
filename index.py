import logging
from flask import Flask, render_template
from generators.SickCreationsAutomation import post_image, create_image, index_files
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
def schedule_post_image():
    db.add_event(event_name="post_image", results=post_image())
    return "Image posted"


@app.route("/create_image", methods=['GET'])
def schedule_create_image():
    db.add_event(event_name="create_image", results=create_image())
    return "Image created"


@app.route("/index_file", methods=['GET'])
def index_file():
    db.add_event(event_name="index_file", results=index_files())
    return "Database updated"


@app.route("/event_store", methods=['GET'])
def event_store():
    results = render_template("events.html", events=db.get_events_list())
    return results


if __name__ == '__main__':
    app.run()
