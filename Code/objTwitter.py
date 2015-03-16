#!/usr/bin/python
#---------
#Object: Twitter
#By Dylan Devalia
#---------

#---------

#Imports

	#Objects
from objLogger import classLogger

	#System
from twython import Twython

#---------

#Main

class classTwitter(object) :
	def __init__(self, apiKey, apiSecret, accessToken, accessTokenSecret, logLevel, logFilePath)	: #Connect to twitter
			#Accesses the twitter account with the two api keys and two access tokens generated per account
		self.api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)
		
			#Sets the log level for the class
		self.logger = classLogger(level = logLevel, filePath = logFilePath)
		self.logger.init("Twitter complete")
	
	def tweet(self, message) : #Tweets message
			#Will tweet the message with the given account
		self.api.update_status(status = message)
	
	def mention(self, name, message) : #Mentions the user followed by the message
			#Will tweet the message, preceded by a mention 
			#	(this will notify the user with the username)
		self.api.update_status(status = "@{:s}: {:s}".format(name, message))
