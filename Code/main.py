#!/usr/bin/python
#---------
#Main Code Loop
#By Dylan Devalia
#---------

#---------

#User configuration - For advanced users only!

	#GPIO pins
pin_button = 14
pin_buzzer = 15
pin_redLed = 27
pin_greenLed = 17
pin_lightDependentResistor = 3
pin_temperatureHumiditySensor = 4
		#LCD display
pin_display_rs = 21
pin_display_e = 26
pin_display_db = [20, 16, 19, 13]

	#Database
database_host = 'localhost'
database_user = 'usrSensor'
database_password = 'raspberry'
database_name = 'dbSensor'
table_name = 'tmp'

	#Twitter
twitter_apiKey = 'N3yJD8TZSofjR1dDcIxCFh2fT'
twitter_apiSecret = 'VJV58qZRuTJHi7vMagi6usZsicwuGbFCyV7tLVhNGOH0r1MFFQ'
twitter_accessToken = '2916185578-11JuSlWm0D9jP2zSqRuLwoi5XL1fasryqmRX1mz'
twitter_accessTokenSecret = 'VPszoWIoIAcxSSdBkJhqGBzoqcxbK1qWca6U0MDYCjIsa'
twitter_mention = 'awade33' #If the values exceed the pre-set values, this account will be notified

	#Min / Max Values
		#Temperature
min_temperature = 15.0
max_temperature = 25.0
		#Humidity
min_humidity = 45.0
max_humidity = 55.0
		#Light
min_light = 25
max_light = 35

	#General
itterations = 10
readingDelay = 600  #Time between readings (seconds)
screenScrollRate = 10 #Time between screen scrolling (seconds)
logLevel = "error" #The depth of log detail show on the console
logFilePath = "logs/" #The directory where the logs will be stored

#---------

#Imports

	#Objects
from objButton import classButton
from objDatabase import classDatabase
from objDelay import classDelay
from objGeneralGPIO import classBuzzer
from objGeneralGPIO import classLed
from objLcd import classLcd
from objLightDependentResistor import classLdr
from objLogger import classLogger
#from objPlotly import classPlotly
from objTempHumidSensor import classThSensor
from objTwitter import classTwitter

	#System Libaries
import time, datetime #Allows access to the time and date of the system
import RPi.GPIO as GPIO #Allows program to interact with the GPIO ports 
import sys #Allows access to system programs
import decimal #Allows mathematical functions

#---------

#Setup

	#GPIO
button = classButton(pin_button, logLevel, logFilePath)
buzzer = classBuzzer(pin_buzzer, logLevel, logFilePath)
redLed = classLed(pin_redLed, logLevel, logFilePath)
greenLed = classLed(pin_greenLed, logLevel, logFilePath)
ldr = classLdr(pin_lightDependentResistor, logLevel, logFilePath)
thSensor = classThSensor(pin_temperatureHumiditySensor, logLevel, logFilePath)
display = classLcd(pin_display_rs, pin_display_e, pin_display_db, logLevel, logFilePath)

db = classDatabase(database_host, database_user, database_password, database_name, logLevel, logFilePath)
twitter = classTwitter(twitter_apiKey, twitter_apiSecret, twitter_accessToken, twitter_accessTokenSecret, logLevel, logFilePath)
delay = classDelay()
logger = classLogger(level = logLevel, filePath = logFilePath)
logger.info("File opened ({:s})".format(logger.getFileName))

logger.init("All complete")

#---------

#Methods

def getReadings() : #Gets readings from the sensors
	temp, humid = thSensor.getReading() #Gets the temperature and humidity
	light = ldr.getReading() #Gets light level
	return temp, humid, light
	
def insertIntoDatabase(table_name, temp, humid, light) : #Tries and catches to insert into the database
	try : #Writing to database
		db.insert(table_name, temp, humid, light)
	except : #Logs if unable to write
		logger.error('Unable to write to database')
		redLed.pulseS(1)

def writeToTwitter(curTime, temp, humid, light) : #Tries and catches to insert into twitter
	try : #Writing to Twitter
		twitter.tweet('Time: {:s}, Temp : {:.1f} *C, Humid: {:.1f} %, Light: {:d} Kohms'.format(curTime, temp, humid, light))
	except : #Logs if unable to write
		logger.error('Unable to write data to Twitter')
		redLed.pulseS(1)
		
def checkTemp(name, temp, curTime, minValue, maxValue) :
	if temp == 0 :
		logger.info("Still gathering average temperature data to analyse")
	elif (temp < minValue) or (temp > maxValue) :
		logger.warning('Temperature exceeding boundaries')
		try : #Write to Twitter
			twitter.mention(name, 'Time: {:s}, WARNING. Temperature at {:.1f}'.format(curTime, temp))
		except : #Logs if unable to write
			logger.error('Unable to message user on Twitter about temperature')
		buzzer.pulseS(1)

def checkHumid(name, humid, curTime, minValue, maxValue) :
	if humid == 0 :
		logger.info("Still gathering average humidity data to analyse")
	elif (humid < minValue) or (humid > maxValue) :
		logger.warning('Humidity exceeding boundaries')
		try : #Write to Twitter
			twitter.mention(name, 'Time: {:s}, WARNING. Humidity at {:.1f}'.format(curTime, humid))
		except : #Logs if unable to write
			logger.error('Unable to message user on Twitter about humidity')
		buzzer.pulseS(1)
		
def checkLight(name, light, curTime, minValue, maxValue) :
	if light == 0 : #Write to Twitter
		logger.info("Still gathering average light data to analyse")
	elif (light < minValue) or (light > maxValue) :
		logger.warning('Light exceeding boundaries')
		try : #Write to Twitter
			twitter.mention(name, 'Time: {:s}, WARNING. Light at {:.1f}'.format(curTime, light))
		except : #Logs if unable to write
			logger.error('Unable to message user on Twitter about light')
		buzzer.pulseS(1)

def averageValue(numNew, num1 = 0, num2 = 0, num3 = 0) : #Generates the average value over 3 readings
		#Daisy chains the last 3 readings
	num3 = num2
	num2 = num1
	num1 = numNew
	
	if (num1 != 0) and (num2 != 0) and (num3 != 0) : #If there have been >= 3 readings
		average = (num1 + num2 + num3) / 3
	else :
		average = 0
	return average, num1, num2, num3
	
#---------
#Main

#db.createTable(table_name)

	#Used to calculate average values
temp1 = 0.0
temp2 = 0.0
temp3 = 0.0
humid1 = 0.0
humid2 = 0.0
humid3 = 0.0
light1 = 0
light2 = 0
light3 = 0

buttonState = button.status()

#while buttonState == False : #Main while loop
for i in range(0, itterations) : #Main while loop (used for testing)

		#Gets readings and current time
	temp, humid, light = getReadings()
	curTime = time.strftime("%H:%M:%S", time.gmtime()) #Gets the current time

	greenLed.pulseS(1) #Pulses green led for user feedback
	logger.data('Temp: {:f}*C; Humid: {:f}%; Light: {:d}Kohms'.format(temp, humid, light)) #Prints to console
	
		#Calculates average values and prints to console
	avgTemp, temp1, temp2, temp3 = averageValue(temp, temp1, temp2, temp3)
	avgHumid, humid1, humid2, humid3 = averageValue(humid, humid1, humid2, humid3)
	avgLight, light1, light2, light3 = averageValue(light, light1, light2, light3)
	logger.data('avgTemp: {:f}, avgHumid: {:f}, avgLight: {:d}'.format(avgTemp, avgHumid, avgLight))
	
		#Checks the readings to see if they exceed boundaries
	checkTemp(twitter_mention, avgTemp, curTime, min_temperature, max_temperature)
	checkHumid(twitter_mention, avgHumid, curTime, min_humidity, max_humidity)
	checkLight(twitter_mention, avgLight, curTime, min_light, max_light)
	
		#Writes to externals
	insertIntoDatabase(table_name, temp, humid, light)
	writeToTwitter(curTime, temp, humid, light)
	
		#Used to scroll information on the display and also allows for button status to be updated
		#	The button status will update every time the screen updates (screenScrollRate)
	for i in range(0, readingDelay / screenScrollRate) :
		buttonState = button.status()

		if buttonState == True :
			break
		elif i % 2 == 0 :
			display.write("Temp : {:.1f} *C\nHumid: {:.1f} %".format(temp, humid))
		else :
			display.write("Light: {:d} Kohms\nTime : {:s}".format(light, curTime))

		delay.second(screenScrollRate)
#---------

#Final

display.write("Closing Program\nGood Bye")
db.close()
delay.second(5)

display.write()
GPIO.cleanup()
logger.info("Closing file")
logger.cleanup()
