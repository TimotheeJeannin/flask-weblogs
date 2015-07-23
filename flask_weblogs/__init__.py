import logging
import time

from os.path import dirname, abspath
import gevent
from gevent.queue import Queue
from flask import Blueprint, render_template, Response

subscriptions = []

# The SSE protocol is described here:
# https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
class ServerSentEvent(object):
    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {self.data: "data", self.event: "event", self.id: "id"}

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) for k, v in self.desc_map.iteritems() if k]
        return "%s\n\n" % "\n".join(lines)


web_logs_blueprint = Blueprint('web_logs', __name__, template_folder=dirname(abspath(__file__)) + '/templates')


@web_logs_blueprint.route("/publish")
def publish():
    def notify():
        msg = str(time.time())
        for sub in subscriptions[:]:
            sub.put(msg)

    gevent.spawn(notify)

    return "OK"


@web_logs_blueprint.route('/subscribe')
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                print 'try to get result'
                result = q.get()
                print 'result ' + result
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit:
            print 'generator exit'
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")


@web_logs_blueprint.route('/')
def index():
    logs = {}
    # for handler in logging.getLogger().handlers:
    #     if hasattr(handler, 'baseFilename'):
    #         with open(handler.baseFilename) as log_file:
    #             logs[handler.baseFilename] = log_file.readlines()

    return render_template('main.jinja2', logs=logs)


class WebLogs(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(web_logs_blueprint, url_prefix='/logs')
