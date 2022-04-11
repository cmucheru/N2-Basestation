
# Python program killing
# a thread using ._stop()
# function
# This kills the program after the period of time denoted as sleep_time (In seconds)
# It determines for how long the relay remains on
# 
  
import time
import threading
import RPi.GPIO as GPIO
sleep_time = 5

class Ignition(threading.Thread):
  
    # Thread class with a _stop() method. 
    # The thread itself has to check
    # regularly for the stopped() condition.
  
    def __init__(self, actuator, pixels, *args, **kwargs):
        super(Ignition, self).__init__(*args, **kwargs)
        self._stop = threading.Event()
        self._actuator = actuator
        pixels.fill((255, 0, 0))
        self._pixels = pixels
  
    # function using _stop function
    def stop(self):
        self._stop.set()
  
    def stopped(self):
        return self._stop.isSet()
  
    def run(self):
        #Turns the relay on
        GPIO.output(self._actuator, GPIO.HIGH)
        #Wait for selected period of time (sleep_time)
        time.sleep(sleep_time)
        #Turn off relay
        while True:
            if self.stopped():
                GPIO.output(self._actuator, GPIO.LOW)
                #Change the color of the pixel led strip
                self._pixels.fill((0,0,255))
                return
  

