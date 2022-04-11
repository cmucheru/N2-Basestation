import os
import sys
import traceback
import time
from main import Operation
from lib import format_exc_for_journald, setup_logging, signalhandler, check_running_instance
import flask
from flask import jsonify, render_template
# from flask_cors import CORS
import logging
import RPi.GPIO as GPIO

app = flask.Flask(__name__)
# CORS(app)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True
app.logger.disabled = True

# TODO there is a big on environment variables fix it
if "DEBUG" in os.environ:
    if os.environ["DEBUG"].lower() == "true":
        DEBUG = True
    elif os.environ["DEBUG"].lower() == "false":
        DEBUG = False
    else:
        raise ValueError(
            "DEBUG environment variable not set to 'true' or 'false'")
else:
    if os.isatty(sys.stdin.fileno()):
        DEBUG = True
    else:
        DEBUG = False

# Script name
script_name = os.path.basename(__file__)
current_dir = os.path.dirname(__file__)

# Get logger
logger = setup_logging(name=script_name, debug=DEBUG)

signalhandler()

# Check if another instance already running #
check_running_instance(filename=script_name)


@app.route('/', methods=['GET'])
def home():
    return "Head over to /api"


@app.route('/api', methods=['GET'])
def api_all():
    val = [{"endpoint": "/api/start_ignition", "description": "starts ignition"},
           {"endpoint": "/api/stop_ignition", "description": "stops ignition"},
           {"endpoint": "/api/start_logging", "description": "starts logging"},
           {"endpoint": "/api/stop_logging", "description": "stops logging"}
           ]
    return render_template("index.html", val=jsonify(val))


@app.route('/api/start_ignition', methods=['GET'])
def start_ignition():
    resp = ops.startignition()
    return jsonify(resp)


@app.route('/api/stop_ignition', methods=['GET'])
def stop_ignition():
    resp = ops.stopignition()
    GPIO.output(19, GPIO.HIGH)
    return jsonify(resp)


@app.route('/api/start_logging', methods=['GET'])
def start_logging():
    resp = ops.startlogging()
    return jsonify(resp)


@app.route('/api/stop_logging', methods=['GET'])
def stop_logging():
    resp = ops.stoplogging()
    return jsonify(resp)


while True:
    try:
        ops = Operation(logger=logger)
        app.run(host='0.0.0.0', debug=False)
    except UserWarning as warn:
        logger.error(warn)
    else:
        logger.error(format_exc_for_journald(
            traceback.format_exc(), indent_lines=False))
        time.sleep(10)
