#!/usr/bin/python
#---------
#Object: LCD
#By Dylan Devalia
#---------

#---------

#Imports

	#Objects
from objLogger import classLogger

	#Libraries
from libAdafruitLcdDisplay import Adafruit_CharLCD

#---------

#Main

class classLcd(Adafruit_CharLCD) :
	def __init__(self, pin_rs, pin_e, pin_db, logLevel, logFilePath) :
			#Calls the '__init__' function of the inherited class
		super(classLcd, self).__init__(pin_rs, pin_e, pin_db)
		
			#Sets the log level for the class
		self.logger = classLogger(level = logLevel, filePath = logFilePath)
		self.logger.init("Display complete (pin_rs, pin_e, pin_db: {:d}, {:d}, {:s})".format(pin_rs, pin_e, pin_db))
		
	def write(self, message = None) : #Writes the messages to the display
		super(classLcd, self).clear()
		if message : #If there is a message
			super(classLcd, self).message(message)
