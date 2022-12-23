from flask import Flask, render_template
import sys
from apps.test_import import TestImport

sys.path.append('../')
app = Flask(__name__)

# If file name is app.py or main.py then project will not start on vercel


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


@app.route("/test")
def test_area():
    TestImport("Did i make mistake?")
    return "test import"


if __name__ == '__main__':
    app.run()
