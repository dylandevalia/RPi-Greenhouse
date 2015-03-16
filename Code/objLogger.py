#!/usr/bin/python
#---------
#Object: Logger
#By Dylan Devalia
#---------

#---------

#Imports

	#System
import time

#---------

#Main

class classLogger(object) :
	def __init__(self, level = None, filePath = None) :
			#Sets the log level to display to console
		if level == 'error' :
			self.level = 5
		elif level == 'warning' :
			self.level = 4
		elif level == 'info' :
			self.level = 3
		elif level == 'init' :
			self.level = 2
		elif level == 'data' :
			self.level = 1
		else :
			self.level = 0
		
			#Stores the current time in the format {Hour:Minute:Second} in the GMT timezone
			#	Used in the log message
		self.curTime = time.strftime('%H:%M:%S', time.gmtime())
		
			#Stores the current date in the format {YearMonthDay-HourMinuteSecond} in the GMT timezone
			#	Used to create a unique file name
		self.curDatetime = time.strftime('%Y%m%d-%H%M%S', time.gmtime())
		
			#Creates a file to store the log messages in
			#	Uses the current date and time for the file name
			#	Also uses the '.log' filetype
		if filePath == None :
			self.fileName = self.curDatetime + ".log"
		else :
			self.fileName = filePath + self.curDatetime + ".log"
		
			#Opens the file in append mode to allow new data to automatically
			#	be added to the end of the file
		self.file = open(self.fileName, "a+")
		
	def getFileName(self) : #Returns the file name used
		nameOfFile = self.fileName
		return nameOfFile
		
	def data(self, message) : #Creates a 'data' level log message
			#Stores the current time
		self.curTime = time.strftime('%H:%M:%S', time.gmtime())
		
			#The 'data' level log message is used to display the peripheral readings
		if self.level >= 1 : #If the set level can display this message
			#Prints to the console
			print '[{:s}] [DATA] {:s}'.format(self.curTime, message)
		
			#Writes message to file regardless of log level
		self.file.write('[{:s}] [DATA] {:s}\n'.format(self.curTime, message))
		
	def init(self, message) : #Creates a 'data' level log message
			#Stores the current time
		self.curTime = time.strftime('%H:%M:%S', time.gmtime())
		
			#The 'init' level log message is used to display the initialisation
			#	messages for each objects and main code
		if self.level >= 2 : #If the set level can display this message
				#Prints to the console
			print '[{:s}] [INIT] {:s}'.format(self.curTime, message)
		
			#Writes message to file regardless of log level
		self.file.write('[{:s}] [INIT] {:s}\n'.format(self.curTime, message))	
		
	def info(self, message) :#Creates a 'info' level log message
			#Stores the current time
		self.curTime = time.strftime('%H:%M:%S', time.gmtime())
			
			#The 'info' level log messages is used for general information from the program
		if self.level >= 3 : #If the set level can display this message
				#Prints to the console
			print '[{:s}] [INFO] {:s}'.format(self.curTime, message)
				
			#Writes message to file regardless of log level
		self.file.write('[{:s}] [INFO] {:s}\n'.format(self.curTime, message))
		
	def warning(self, message) :#Creates a 'warning' level log message
			#Stores the current time
		self.curTime = time.strftime('%H:%M:%S', time.gmtime())
		
			#The 'warning' level log messages is used for when specific functions do not work
			#	or have crashed but have not stopped the program
		if self.level >= 4 : #If the set level can display this message
				#Prints to the console
			print '[{:s}] [WARNING] {:s}'.format(self.curTime, message)
				
			#Writes message to file regardless of log level
		self.file.write('[{:s}] [WARNING] {:s}\n'.format(self.curTime, message))
	
	def error(self, message) :#Creates a 'error' level log message
			#Stores the current time
		self.curTime = time.strftime('%H:%M:%S', time.gmtime())
		
			#The 'error' level log messages is used when the program has stopped working
		if self.level >= 5 : #If the set level can display this message
				#Prints to the console
			print '[{:s}] [ERROR] {:s}'.format(self.curTime, message)
				
			#Writes message to file regardless of log level
		self.file.write('[{:s}] [ERROR] {:s}\n'.format(self.curTime, message))
		
	def cleanup(self) : #Closes the open file
		self.file.close()
