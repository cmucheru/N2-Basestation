
# Python program killing
# a thread using ._stop()
# function
 
import time
import threading
import RPi.GPIO as GPIO
import numpy as np
import random
from datetime import datetime
from logData import Publish

class FetchData(threading.Thread):
  
    # Thread class with a _stop() method. 
    # The thread itself has to check
    # regularly for the stopped() condition.
  
    def __init__(self, ser, *args, **kwargs):
        super(FetchData, self).__init__(*args, **kwargs)
        self._stop = threading.Event()
        self._ser = ser
        self.publisher = Publish()
  
    # function using _stop function
    def stop(self):
        self._stop.set()
  
    def stopped(self):
        return self._stop.isSet()
    
    #The above are initialization functions for a threaded program
    
    def run(self):
        # TODO implement cython arrays to boost the efficiency
        allPoints = []
        time.sleep(2)
        while True:
            #Read data from serial - Stays in this loop forever.
            val = self._ser.readline().decode('utf-8').rstrip()
            self.publisher.Publish(val)
            allPoints.append(val)
            time.sleep(0.0125)
            if self.stopped():
                #Store the data in a csv file - labelled according to the name
                filename = datetime.now().strftime("%A %d %B %Y %I-%M%p") + ".csv"
                np.savetxt(filename, allPoints, newline="\n", fmt='%s')
                return
  


