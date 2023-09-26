import logging
from flask import Flask, render_template
from generators.SickCreationsAutomation import post_image, create_image
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

scheduler = BackgroundScheduler()
scheduler.add_job(create_image, 'interval', minutes=5)
scheduler.add_job(post_image, 'interval', minutes=10)
scheduler.start()


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


if __name__ == '__main__':
    app.run()
