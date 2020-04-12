from datetime import datetime

from flask import Flask, jsonify, request, render_template

from .api_v1 import api_v1
from .api_helpers import write_log_to_file


api = Flask(__name__)
api.config.from_object('config')
api.url_map.strict_slashes = False
api.register_blueprint(api_v1)

endpoint_log = {}


@api.before_request
def fetch_request_details():
    """fetch the request details and set
    to endpoint log
    """
    endpoint_log['method'] = request.method
    endpoint_log['endpoint'] = request.path
    endpoint_log['time_accessed_timestamp'] = datetime.utcnow().timestamp()


@api.after_request
def set_response_status_code(response):
    """Set the response status code in the endpoint log
    """
    endpoint_log['status_code'] = response.status_code
    return response


@api.teardown_request
def save_logs_here(error=None):
    current_now = datetime.utcnow().timestamp()
    a = current_now - endpoint_log['time_accessed_timestamp']
    endpoint_log['time_elapsed_milliseconds'] = f'{(a * 1000):.3f} ms'
    write_log_to_file(**endpoint_log)
    endpoint_log.clear()


@api.route('/', methods=('GET',))
def welcome():
    return render_template('index.html')


