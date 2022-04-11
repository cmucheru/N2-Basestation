import os
import time
import json
import queue
import serial
import threading
from datetime import datetime
from publisher import TestPublisher

# TODO Setup as environment variable
WRITE_FILE_DURATION = 60
ESTIMATED_DURATION = 3600


class FetchData:

    def __init__(self, logger):
        """
        This initializes the fetch data class
        :param logger: Logger
        """
        self.logger = logger
        self.serial = None
        self.find_serial()
        self.publisher = TestPublisher(logger=self.logger)
        self.running = False
        # TODO compare different queues to see which one works best e.g circular queues
        self.dataqueue = queue.Queue()
        # TODO implement cython arrays to boost the efficiency
        self.datapoints = []
        self.maximum_val = 0
        self.cwd = os.path.dirname(__file__)
        self.filename = str(self.cwd) + "/" + datetime.now().strftime("%A_%d_%B_%Y_%H_%M_%S") + ".csv"
        self.readthread = threading.Thread(target=self.read_data)
        self.savethread = threading.Thread(target=self.save_data)
        self.loggingthread = threading.Thread(target=self.check_logging)
        self.stopthread = threading.Thread(target=self.stop)
        self.readthread.setDaemon(True)
        self.savethread.setDaemon(True)
        self.loggingthread.setDaemon(True)
        self.stopthread.setDaemon(True)

    def find_serial(self):
        """
        This method searches the available serial port and see which one it connected and sending data
        It will set serial to the one that is available an plugged in
        :return: None
        """
        SERIAL_PORTS = ['/dev/ttyUSB1', '/dev/ttyUSB0', '/dev/ttyACM1', '/dev/ttyACM0']
        for port in SERIAL_PORTS:
            try:
                self.serial = serial.Serial(port=port, baudrate=9600)
            except serial.serialutil.SerialException as e:
                self.logger.error(e)
            else:
                break

    def check_logging(self):
        """
        This method checks the "sensorData/internals" topic to see if a message has been published to that we can
        start logging data. It will wait for the action: Started logging with logging status set to True
        :return:
        """
        count = 0
        while True:
            try:
                message = json.loads(str(self.publisher.check_message))
                # If we find the message corresponding with start logging we break and return True
                if str(message['data']['action']) == "Started logging" and str(
                        message['data']['logging status']) == "True":
                    break
            except json.decoder.JSONDecodeError as e:
                # TODO find a better way to log the error once
                if count == 0:
                    # Logs the error once
                    self.logger.error("Check logging error: {}".format(e))
                    count = count + 1
            time.sleep(1)
        self.running = True
        return True

    def save_data(self):
        """
        This saves data to the csv file in batches. When we receive an array of data points from the queue we read that
        data while appending it to the file.
        We save the data only if we have started self.running and we stop once we set False to self.running
        """
        self.logger.info("Started saving data thread")
        while self.running:
            time.sleep(1)
            while not self.dataqueue.empty():
                datapoints = self.dataqueue.get()
                maximum_val = max(datapoints)
                if self.maximum_val < maximum_val:
                    self.maximum_val = maximum_val
                with open(self.filename, "a+") as f:
                    for i in datapoints:
                        f.write("{}\n".format(i))
                self.logger.debug("Saved batched data")
                new_filename = str(self.cwd) + "/" + str(maximum_val) + "_" + datetime.now().strftime(
                    "%A_%d_%B_%Y_%H_%M_%S") + ".csv"
                os.rename(self.filename, new_filename)
                self.filename = new_filename
                if not self.running:
                    return

    def read_data(self):
        """
        This reads data from the serial port
        We first reset the input buffer then we started reading data from the serial port
        We send the data to an array as well to our message broker
        After 60 seconds, WRITE_FILE_DURATION we write the data to a queue where we will save it to a csv file
        We read the data only if we have started self.running and we stop once we set False to self.running
        """
        self.logger.info("Started reading data thread")
        self.serial.reset_input_buffer()
        while self.running:
            start_time = time.time()
            elapsed_time = 0
            while elapsed_time <= WRITE_FILE_DURATION:
                try:
                    val = self.serial.readline().decode('utf-8').rstrip()
                except UnicodeDecodeError as e:
                    self.logger.error(e)
                    val = 0.0
                except ValueError as e:
                    self.logger.error(e)
                    val = 0.0
                if elapsed_time == 0:
                    self.logger.info("Inserting the first value")
                self.datapoints.append(val)
                self.publisher.run(val)
                elapsed_time = time.time() - start_time
            self.dataqueue.put(self.datapoints)
            self.datapoints = []
            self.logger.debug("Sent batched data to queue")
            if not self.running:
                return

    def run(self):
        self.logger.info("Started reading serial service")
        self.readthread.start()
        self.savethread.start()
        self.loggingthread.start()
        self.stopthread.start()
        self.readthread.join()

    def stop(self):
        """
        This method checks the "sensorData/internals" topic to see if a message has been published to that we can
        stop logging data. It will wait for the action: Stopped logging with logging status set to False
        """
        count = 0
        while True:
            try:
                message = json.loads(str(self.publisher.check_message))
                if str(message['data']['action']) == "Stopped logging" and str(
                        message['data']['logging status']) == "False":
                    self.logger.info("Stopped Service")
                    break
            except json.decoder.JSONDecodeError as e:
                if count == 0:
                    self.logger.error("Check logging error: {}".format(e))
                    count = count + 1
            time.sleep(1)

        self.running = False
        self.readthread.join()
        self.savethread.join()
        raise UserWarning("Stopped Service")


def main(logger):
    fetch_data = FetchData(logger=logger)
    while True:
        if fetch_data.check_logging():
            break
    fetch_data.run()
    time.sleep(ESTIMATED_DURATION)
