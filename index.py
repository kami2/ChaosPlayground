from flask import Flask, render_template
from apps.test_import import TestImport

app = Flask(__name__)


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


if __name__ == '__main__':
    app.run()
