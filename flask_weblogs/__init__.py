import logging
import subprocess
import threading

from os.path import dirname, abspath
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


def tail_files(file_paths):
    def tail_file(file_path):
        process = subprocess.Popen('tail -f ' + file_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            new_log_line = process.stdout.readline()
            for sub in subscriptions[:]:
                sub.put(new_log_line)

    for path in file_paths:
        thread = threading.Thread(target=tail_file, args=(path,))
        thread.daemon = True
        thread.start()


@web_logs_blueprint.route('/subscribe')
def subscribe():
    def event_generator():
        queue = Queue()
        subscriptions.append(queue)
        try:
            while True:
                result = queue.get()
                event = ServerSentEvent(str(result))
                yield event.encode()
        except GeneratorExit:
            subscriptions.remove(queue)

    return Response(event_generator(), mimetype="text/event-stream")


@web_logs_blueprint.route('/')
def index():
    logs = {}
    return render_template('main.jinja2', logs=logs)


class WebLogs(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(web_logs_blueprint, url_prefix='/logs')
        log_files = []
        for handler in logging.getLogger().handlers:
            if hasattr(handler, 'baseFilename'):
                log_files.append(handler.baseFilename)
        tail_files(log_files)
