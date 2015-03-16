#!/usr/bin/python
#---------
#Object: Database
#By Dylan Devalia
#---------

#---------

#Imports

	#Objects
from objLogger import classLogger
	
	#System
import MySQLdb as sql

#---------

#Main

class classDatabase(object) :
	def __init__(self, host, username, password, database, logLevel, logFilePath) :
			#Connect to database
		self.db = sql.connect(host, username, password, database)
		self.cur = self.db.cursor()
		self.database = database
		
			#Sets the log level for the class
		self.logger = classLogger(level = logLevel, filePath = logFilePath)
		self.logger.init("Database complete (db: {:s})".format(database))
		
	def insert(self, tableName, temp, humid, light) : #Inserts data into table
		self.cur.execute("""INSERT INTO tbl_%s (temperature, humidity, light)
							VALUES (%f, %f, %d)
							""" %(tableName, temp, humid, light)
							)
		self.db.commit()
		
	def createTable(self, tableName) : #Creates a table
		self.cur.execute("""IF NOT EXISTS (SELECT * FROM sys.objects
							WHERE object_id = OBJECT_ID(N'%s.tbl_%s') AND type in (N'U'))
							BEGIN
								CREATE TABLE %s.tbl_%s(
									id INT PRIMARY KEY AUTO_INCREMENT,
									curTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
									temperature FLOAT,
									humidity FLOAT,
									light INT
									)
							END""" %(self.database, tableName, self.database, tableName)
							)
	
	def dropTable(self, tableName) : #Drops table if it exists
		self.cur.execute("DROP TABLE IF EXISTS tbl_%s" %tableName)
		
	def select(self, select, fromTable, where) : #Gets value(s) from table
		result = self.cur.execute(	"SELECT %s"
									"FROM %s "
									"WHERE %s",
									(select, fromTable, where)
									)
		return result
		
	def close(self) : #Safely closes the connections from the database
		self.cur.close()
		del self.cur
		self.db.close()
