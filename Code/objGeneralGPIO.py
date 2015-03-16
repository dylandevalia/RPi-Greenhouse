#!/usr/bin/python
#---------
#Object: GPIO
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

	#General
class classGPIO(object) :
	def __init__(self, pin, logLevel, logFilePath) :
			#Specify board type
		GPIO.setmode(GPIO.BCM)
		
		    #Set GPIO warnings false
		GPIO.setwarnings(False)
		
		    #Constants for led-pin
		self.pin = pin
		
		    #Define pin functions
		GPIO.setup(pin,GPIO.OUT)
		
			#Sets the log level for the class
		self.logger = classLogger(level = logLevel, filePath = logFilePath)
			
	def on(self) : #Turns GPIO on
		GPIO.output(self.pin, GPIO.HIGH)
	
	def off(self) : #Turns GPIO off
		GPIO.output(self.pin, GPIO.LOW)
		
	def pulseMS(self, length) : #Pulses GPIO (milliseconds)
		self.on()
		delay.millisecond(length)
		self.off()
	
	def pulseS(self, length) : #Pulses GPIO (seconds)
		self.on()
		delay.second(length)
		self.off()
		
	def loopMS(self, iteration, length, lag = 1000) : #Loops GPIO (milliseconds)
		for i in range(0, iteration) :
			self.pulseMS(length)
			delay.millisecond(lag) #Time till next loop

	def loopS(self, iteration, length, lag = 1) : #Loops GPIO (seconds)
		for i in range(0, iteration) :
			self.pulseS(length)
			delay.second(lag) #Time till next loop

	#LED
class classLed(classGPIO) :
	def __init__(self, pin, logLevel, logFilePath) :
			#Calls the '__init__' function of the inherited class
		super(classLed, self).__init__(pin, logLevel, logFilePath)
		self.logger.init("Led complete (pin: {:d})".format(pin))
		
	#Buzzer
class classBuzzer(classGPIO) :
	def __init__(self, pin, logLevel, logFilePath) :
			#Calls the '__init__' function of the inherited class
		super(classBuzzer, self).__init__(pin, logLevel, logFilePath)
		self.logger.init("Buzzer complete (pin: {:d})".format(pin))

	def sos(self) :
		super(classBuzzer, self).loopS(3, 1, 1)
		super(classBuzzer, self).loopS(3, 2, 1)
		super(classBuzzer, self).loopS(3, 1, 1)
	
	def q(self) :
		super(classBuzzer, self).on()
		delay.second(1)
		super(classBuzzer, self).off()
		