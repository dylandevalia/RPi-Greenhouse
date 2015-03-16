#!/usr/bin/python
#---------
#Object: Temperature and Humidity Sensor
#By Dylan Devalia
#---------

#---------

#Imports

	#Objects
from objLogger import classLogger

	#System
import Adafruit_DHT as sensor

#---------

#Main

class classThSensor(object) :
	def __init__(self, pin, logLevel, logFilePath) :
		self.pin = pin
		
			#Sets the log level for the class
		self.logger = classLogger(level = logLevel, filePath = logFilePath)
		self.logger.init("ThSensor complete (pin: {:d})".format(pin))
	
	def getReading(self) : #Returns current temperature and humidity levels
		humidity, temperature = sensor.read_retry(sensor.AM2302, self.pin)
		return temperature, humidity
	
	def getTemp(self) : #Returns current temperature level
		humidity, temperature = sensor.read_retry(sensor.AM2302, self.pin)
        	return temperature
	
	def getHumid(self) : #Returns current humidity level
		humidity, temperature = sensor.read_retry(sensor.AM2302, self.pin)
		return humidity
