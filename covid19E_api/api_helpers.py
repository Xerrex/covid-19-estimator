import os
import xml.etree.ElementTree as Et

from flask import jsonify


def method_not_allowed_405():
    """Method not allowed 405
    """
    return jsonify({
        "message": "Method Not allowed"
    }), 405


def write_log_to_file(**endpoint_log):

    """Writes logs to a txt file

    :keyword Arguments
    - method {str:string} - the http verb used to make request.
    - endpoint {str:string} - the url used to make the request.
    - status_code {int:integer} - the http status code of the response.
    - time_elapsed_milliseconds' - time in milliseconds it took to handle request
    """

    method = endpoint_log['method']
    endpoint = endpoint_log['endpoint']
    status_code = endpoint_log['status_code']
    time_elapsed = endpoint_log['time_elapsed_milliseconds']
    log_txt = f"{method}\t\t{endpoint}\t\t{status_code}\t\t{time_elapsed}"

    if os.path.exists('endpoint_logs.txt'):
        with open('endpoint_logs.txt', 'a') as log_appender:
            log_appender.write(f"\n{log_txt}")
    else:
        with open('endpoint_logs.txt', 'w') as log_writer:
            log_writer.write(log_txt)


def read_log_to_file(path='endpoint_logs.txt'):
    """Read log file entries

    :param path: {str:string} - path to log file:
    :return: list or None
    """
    if os.path.exists(path):
        with open(path , 'r') as log_reader:
            logs = log_reader.readlines()
        return logs
    return None


def estimates_xml_serializer(estimates):
    """Create an xml document from estimates

    Expected data:
    {
      "data": {
        "periodType": "days",
        "population": 66622705,
        "region": {
          "avgAge": 19.7,
          "avgDailyIncomeInUSD": 5,
          "avgDailyIncomePopulation": 0.71,
          "name": "Africa"
        },
        "reportedCases": 674,
        "timeToElapse": 58,
        "totalHospitalBeds": 1389614
      },
      "impact": {
        "casesForICUByRequestedTime": 176685056,
        "casesForVentilatorsByRequestedTime": 70674022,
        "currentlyInfected": 6740,
        "dollarsInFlight": 727589060608.0,
        "hospitalBedsByRequestedTime": -529568803,
        "infectionsByRequestedTime": 3533701120,
        "severeCasesByRequestedTime": 530055168
      },
      "severeImpact": {
        "casesForICUByRequestedTime": 883425280,
        "casesForVentilatorsByRequestedTime": 353370112,
        "currentlyInfected": 33700,
        "dollarsInFlight": 3637945303040.0,
        "hospitalBedsByRequestedTime": -2649789475,
        "infectionsByRequestedTime": 17668505600,
        "severeCasesByRequestedTime": 2650275840
      }
    }
    """

    # create root element: <data></data>
    root = Et.Element('data')

    # get the children: data, Impact, severeImpact
    for child_key, child_value in estimates.items():

        # create child ie. <impact></impact>,
        child_element = Et.SubElement(root, child_key)

        # get the grandChildren(key, value) ie. estimates['impact'].items()
        for grand_c_key, grand_c_value in child_value.items():

            # create grand child element
            # ie. <currentlyInfected> </currentlyInfected>
            grand_child_element = Et.SubElement(child_element, grand_c_key)

            # handle estimates['data']['region'] since it
            # has children.
            # consider using try/catch block in future
            if grand_c_key == "region":
                for key, value in grand_c_value.items():

                    # create great grand child element
                    # ie. <name> africa <name>
                    great_gc_element = Et.SubElement(grand_child_element, key)
                    great_gc_element.text = str(value)
            else:
                # grand children with no children
                grand_child_element.text = str(grand_c_value)

    return Et.tostring(root, encoding='utf8')
