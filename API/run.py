"""API entry_point
"""


from API.covid19EAPI.api import api


if __name__ == '__main__':
    api.run(debug=True)
