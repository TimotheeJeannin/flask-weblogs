import logging
from os.path import dirname, abspath

from flask import jsonify, Blueprint, render_template

web_logs_blueprint = Blueprint('web_logs', __name__, template_folder=dirname(abspath(__file__)) + '/templates')


@web_logs_blueprint.route('/')
def index():
    logs = {}
    for handler in logging.getLogger().handlers:
        if hasattr(handler, 'baseFilename'):
            with open(handler.baseFilename) as log_file:
                logs[handler.baseFilename] = log_file.readlines()

    return render_template('main.jinja2', logs=logs)


class WebLogs(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(web_logs_blueprint, url_prefix='/web_logs')
