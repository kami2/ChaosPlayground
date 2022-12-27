from flask import Flask, render_template
from apps.test_import import TestImport
from helpers.database_helper import DatabaseHelper

app = Flask(__name__)


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
        return f"Connection error: {e}"

    return msg


if __name__ == '__main__':
    app.run()
