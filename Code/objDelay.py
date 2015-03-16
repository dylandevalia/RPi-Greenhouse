#!/usr/bin/python
#---------
#Object: Delay
#By Dylan Devalia
#---------

#---------

#Imports

	#Objects
from objLogger import classLogger

    #System
import time

#---------

#Main

class classDelay(object) :
	def __init__(self) :
		#No initialisation required
		pass
	
	def millisecond(self, length) : #Delay in milliseconds
		delay = length/1000
		time.sleep(delay)
	
	def second(self, length) : #Delay in seconds
	        delay = length
        	time.sleep(delay)
	
	def minute(self, length) : #Delay in minutes
	        delay = length*60
        	time.sleep(delay)
	
	def hour(self, length) : #Delay in hours
	        delay = length*60*60
        	time.sleep(delay)
	
	def day(self, length) : #Delay in days
	        delay = length*60*60*24
        	time.sleep(delay)

