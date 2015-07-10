import logging

from flask import jsonify, Blueprint

web_logs_blueprint = Blueprint('web_logs', __name__)


@web_logs_blueprint.route('/')
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
        app.register_blueprint(web_logs_blueprint)
