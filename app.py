from flask import Flask

app = Flask(__name__)

# If file name is app.py or main.py then project will not start on vercel

@app.route("/")
def main():
    return "Alive"


@app.route("/test")
def test_area():
    return "Chaotic evil"


if __name__ == '__main__':
    app.run()
