import logging
from flask import Flask, render_template, request
from apps.test_import import TestImport
from helpers.database_helper import DatabaseHelper
from apps.ImageGenerator import ImageGenerator

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


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
