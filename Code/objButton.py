#!/usr/bin/python
#---------
#Object: Button
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

#Main

class classButton(object) :
	def __init__(self, pin, logLevel, logFilePath) :
			#Specify board type
		GPIO.setmode(GPIO.BCM)
		
		    #Set GPIO warnings false
		GPIO.setwarnings(False)
		
			#Constants
		self.pin = pin
	        	
			#Define pin functions
		GPIO.setup(pin,GPIO.IN)
		
			#Sets the log level for the class
		self.logger = classLogger(level = logLevel, filePath = logFilePath)
		self.logger.init("Button complete (pin: {:d})".format(pin))
		
	def status(self) : #Returns the status of the button
		buttonStatus = GPIO.input(self.pin)
		if buttonStatus == True :
			return False
		else :
			return True
	
	def waitForPress(self) : #Keeps running until the button is pre
		while True :
			if status() == True :
				delay.millisecond(100)
			else :
				return True
