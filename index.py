from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return "Alive"


@app.route("/test")
def test_area():
    return "Chaotic evil"


if __name__ == '__main__':
    app.run()
