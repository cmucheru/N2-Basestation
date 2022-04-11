import logging
import signal
import socket
import sys
import os
from logging import Logger

logger = logging.getLogger(f"main.{__name__}")


# TODO add in combined utils
def setup_logging(name, debug):
    """
    Setups logging for the process
    :param name: This is the name to setup logging with
    :param debug: If debug is set to true or false
    :type name: string
    :type debug: bool
    """
    filename = "{}/{}.log".format(os.path.dirname(__file__), str(name).lower())
    logger: Logger = logging.getLogger(name)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler(filename)
    consoleHandler = logging.StreamHandler()
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    return logger


def format_exc_for_journald(ex, indent_lines=False):
    """
    Journald removes leading whitespace from every line, making it very
    hard to read python traceback messages. This tricks journald into
    not removing leading whitespace by adding a dot at the beginning of
    every line
    :param ex: Error lines
    :param indent_lines: If indentation of lines should be present or not
    :type indent_lines: bool
    """
    result = ''
    for line in ex.splitlines():
        if indent_lines:
            result += ".    " + line + "\n"
        else:
            result += "." + line + "\n"
    return result.rstrip()


def signal_handler(*_):
    logger.debug("\nExiting...")
    sys.exit(0)


def signalhandler():
    """
    This handle SIGTERM and SIGINT signals
    :return:
    """
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def check_running_instance(filename):
    """
    Since systemd will never run 2 instances of a service at once, the only
    time this would happen is if a service was running, and someone tried to
    run the script manually from terminal at the same time
    :param filename: The filename of the current running file
    :return: None
    """

    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + filename)
    except socket.error:
        logger.error(f"Another instance of {filename} is already running")
        sys.exit(1)
