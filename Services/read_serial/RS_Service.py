#!/usr/bin/env python3
import os
import sys
import traceback
import time
from main import main
from lib import format_exc_for_journald, setup_logging, signalhandler, check_running_instance

# TODO there is a big on environment variables fix it

# If the DEBUG environment variable is set, uses that to set the DEBUG
# global variable
# If the environment variable isn't set, only sets DEBUG to True if we're
# running in a terminal (as opposed to systemd running our script)
if "DEBUG" in os.environ:
    # Use Environment Variable
    if os.environ["DEBUG"].lower() == "true":
        DEBUG = True
    elif os.environ["DEBUG"].lower() == "false":
        DEBUG = False
    else:
        raise ValueError("DEBUG environment variable not set to 'true' or 'false'")
else:
    # Use run mode
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

while True:
    try:
        main(logger=logger)
    except UserWarning as warn:
        logger.error(warn)
        break
    else:
        logger.error(format_exc_for_journald(traceback.format_exc(), indent_lines=False))
        time.sleep(10)
