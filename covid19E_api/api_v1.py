from flask import Blueprint, request, jsonify, \
    make_response

from src.estimator import estimator

from .api_helpers import method_not_allowed_405, \
    estimates_xml_serializer, read_log_to_file

api_v1 = Blueprint('api_v1',  __name__, url_prefix='/api/v1')


@api_v1.route('/on-covid-19/', methods=('GET', 'POST'))
@api_v1.route('/on-covid-19/<res_format>', methods=('GET', 'POST'))
def covid19_estimator(res_format='json'):
    """Handles POST request to the covid19 estimator

    :param res_format: {str:string} - name of response format
    :return: a response formatted as per the res_format param
    """

    if request.method == 'POST':
        if request.data:
            res_data = request.get_json()
            estimates = estimator(res_data)

            if res_format.lower() == 'json':
                return jsonify(estimates), 200

            elif res_format.lower() == 'xml':
                estimates_xml = estimates_xml_serializer(estimates)
                res = make_response(estimates_xml)
                res.mimetype = 'application/xml'
                res.headers["Content-Type"] = "application/xml; charset=utf-8"
                return res

            return jsonify(
                estimates,
                message = f"'{res_format}' response format not supported"
            ), 400
        return jsonify(
            data={},
            message="Empty data was presented"
        ), 400

    return method_not_allowed_405()


@api_v1.route('/on-covid-19/logs', methods=('GET',))
def covid19_logs():
    """Handles a GET request to access the API Logs

    :return: string response
    """
    if request.method == 'GET':
        if read_log_to_file('endpoint_logs.txt'):
            logs = read_log_to_file('endpoint_logs.txt')
            log_text = ''
            for log in logs:
                log_text += f"{log}"
            res = make_response(log_text)
            res.mimetype = 'application/text'
            res.headers["Content-Type"] = "text/plain;"
            return res
        else:
            res = make_response("logs are empty")
            res.mimetype = 'application/text'
            res.headers["Content-Type"] = "text/plain;"
            return res
    else:
        return method_not_allowed_405()
