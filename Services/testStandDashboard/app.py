'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from ignition import *
from dataFetcher import *
import board
import neopixel
import serial

import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define actuators GPIOs Relay
ledRed = 19

#define neopixels
pixels = neopixel.NeoPixel(board.D18, 8)

#set up serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

#initialize GPIO status variables
ledRedSts = 0

# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   

# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)

testNum = 0

ignitionThreads = []
dataThreads = []

@app.route("/")
def index():
	global testNum
	# Read GPIO Status
	ledRedSts = GPIO.input(ledRed)

	pixels.fill((75,0,130))

	templateData = {
      'ledRed'  : ledRedSts,
	  'testNum' : testNum,
      }
	return render_template('index.html', **templateData)
	
# The function below is executed when someone requests a URL with the actuator name and action in it:
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	global testNum
	if deviceName == 'ledRed':
		actuator = ledRed
   
	if action == "on":
		ser.flush()
		t1 = Ignition(actuator, pixels)
		ignitionThreads.append(t1)
		ignitionThreads[testNum].start()
		data = FetchData(ser)
		dataThreads.append(data)
		dataThreads[testNum].start()
		ignitionThreads[testNum].stop()
		testNum = testNum + 1

	if deviceName == 'stopData':
		dataThreads[testNum - 1].stop()
		pixels.fill((75,0,130))

	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	ledRedSts = GPIO.input(ledRed)
   
	templateData = {
      'ledRed'  : ledRedSts,
	  'testNum' : testNum,
	}
	return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
