#!/usr/bin/python
#---------
#Object: Light Dependent Resistor
#By Dylan Devalia
#---------

#---------

#Imports

	#Objects
from objDelay import classDelay
from objLogger import classLogger

	#System
import RPi.GPIO as GPIO

#---------

#Setup

delay = classDelay()

#---------

class classLdr(object) :
	def __init__(self, pin, logLevel, logFilePath) :
			#Specify board type
		GPIO.setmode(GPIO.BCM)
		
			#Set GPIO warnings false
		GPIO.setwarnings(False)
		
		#Constants for led-pin
		self.pin = pin
		
			#Sets the log level for the class
		self.logger = classLogger(level = logLevel, filePath = logFilePath)
		self.logger.init("Ldr complete (pin: {:d})".format(pin))
	
	def getReading(self) : #Returns current light level
		reading = 0
		
			#Sets the pin has an output peripheral and sets a low current
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, GPIO.LOW)
		delay.second(3) #Waits for the pin to discharge
		
			#Sets the pin as an input
		GPIO.setup(self.pin, GPIO.IN)
		
			#Counts up until the sensor gives off a low signal`
		while (GPIO.input(self.pin) == GPIO.LOW) :
			reading += 1
			
		return reading
		