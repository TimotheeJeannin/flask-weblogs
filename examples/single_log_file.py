import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, redirect
from flask.ext.weblogs import WebLogs

formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', '%a, %d %b %Y %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler('logs.txt', maxBytes=1024 * 1024 * 10)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)
logging.getLogger().addHandler(file_handler)

app = Flask(__name__)
WebLogs(app)


@app.route("/")
def hello():
    return redirect('logs')


if __name__ == "__main__":
    app.run(debug=True)
