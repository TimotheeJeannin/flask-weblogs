import logging
from logging.handlers import RotatingFileHandler

from os.path import dirname, abspath
from flask import Flask, make_response, request
from flask.ext.weblogs import WebLogs
from gevent.pywsgi import WSGIServer

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
def index():
    return make_response(open(dirname(abspath(__file__)) + '/index.html').read())


@app.route('/log/<level>', methods=['POST'])
def log(level):
    app.logger.log(int(level), request.get_data())
    return ''


if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
