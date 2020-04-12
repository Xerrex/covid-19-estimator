"""Hold the app configuration
"""
import os

SECRET_KEY = os.getenv('SECRET_KEY') or 'ThisIsAnAwesomeKeyButConsiderProvidingYours'
JSON_SORT_KEYS = False
JSONIFY_PRETTYPRINT_REGULAR = True