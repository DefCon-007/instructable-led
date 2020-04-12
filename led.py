from flask import Flask, render_template, request, jsonify, redirect
import rgbStrip
import RPi.GPIO as GPIO

from threading import Thread
import json 
import time 

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

monitorTop = [0, 0, 125]
monitorBottom = [0, 0, 125]
monitorLeft = [0, 0, 125]
monitorRight = [0, 0, 125]

timeOn = 0.05
timeOff = 0.08


LED_COUNT = 40

rbgObject = rgbStrip.rgb(GPIO, LED_COUNT)

pixels = rbgObject.pixels
pixels.clear()
pixels.show()  

randomFlag = True

@app.route('/randomcoloron')
def randomcolor() : 
	global randomFlag
	randomFlag = True
	t1 = Thread(target=flashrandomlightsmonitor)
	t1.start()
	return render_template("index.html",pin_data={})

@app.route('/randomcoloroff') 
def randcoloroff() :
	global randomFlag 
	randomFlag = False
	return render_template("index.html",pin_data={})


def flashrandomlightsmonitor() :
	while randomFlag :
		setAllMonitor()
		time.sleep(timeOn)
		rbgObject.clearAllMonitor()
		time.sleep(timeOff)

@app.route('/setColors', methods=["POST"])
def setAllColors():
	global monitorRight, monitorTop, monitorLeft, monitorBottom, timeOn, timeOff
	data = json.loads(request.data)

	m = data["rgbmonitorTop"].split(",")
	monitorTop = [int(float(m[0])), int(float(m[1])), int(float(m[2]))]
	m = data["rgbmonitorBottom"].split(",")
	monitorBottom = [int(float(m[0])), int(float(m[1])), int(float(m[2]))]

	m = data["rgbmonitorLeft"].split(",")
	monitorLeft = [int(float(m[0])), int(float(m[1])), int(float(m[2]))]

	m = data["rgbmonitorRight"].split(",")
	monitorRight = [int(float(m[0])), int(float(m[1])), int(float(m[2]))]

	timeOn = float(data["timeOn"])
	timeOff = float(data["timeOff"])
	setAllMonitor()
	return "ok"

def setAllMonitor() :
	rbgObject.setMonitorTop(*monitorTop)
	rbgObject.setMonitorBottom(*monitorBottom)
	rbgObject.setMonitorLeft(*monitorLeft)
	rbgObject.setMonitorRight(*monitorRight)


@app.route('/')
def index():
	return render_template('index.html', pin_data={})



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=1234, debug=True)
