import logging
from flask import jsonify


def index():
    logs = {}
    for handler in logging.getLogger().handlers:
        if hasattr(handler, 'baseFilename'):
            with open(handler.baseFilename) as log_file:
                logs[handler.baseFilename] = log_file.readlines()

    return jsonify(logs)


class WebLogs(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule('/weblogs', 'index', index)
