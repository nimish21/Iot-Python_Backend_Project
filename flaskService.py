#+=============================================================+
#
#    Project Title   : Python Backend Assignment
#    Client Company  : Shoreline IOT
#    Script Name     : flaskService.py
#
#    Programming Language : Python
#    Python Version     : 3.9.1
#
#    Developed By, Nimish Nirmal
#				   Mail : nimishnirmalbiz@gmail.com
#
#    Date of Creation : 27 March 2022
#          
#    Libraries : Refer Requirments.txt
#    Guidelines: Refer README.Md
#
#+=============================================================+

#!/bin/python3

''' Import Python Libraries '''
# Import Python Internal Libraries
import os
import sys
import time
import markdown
import datetime

# Import the Framework and Required Libraries
from flask import Flask, jsonify, request

# Import the Flask MySQL Library
from flask_mysqldb import MySQL

''' Flask Application '''
# Create an instance of Flask
app = Flask(__name__)

''' MySQL Object '''
#For Localhost MySQL Connection
mysqlHost = "localhost"
mysqlUser = "root"
mysqlPassword = ""
mysqlDatabase = "shorelineiot"
mysqlTable = "devices"

# For Remote MySQL Connection
# mysqlHost = "remotemysql.com"
# mysqlDatabase = "E256GsyfOS "
# mysqlUser = "E256GsyfOS "
# mysqlPassword = "JrV4iKvKHe"
# mysqlTable = "devices"

# Configure Flask MySQL 
app.config['MYSQL_HOST'] = mysqlHost
app.config['MYSQL_USER'] = mysqlUser
app.config['MYSQL_PASSWORD'] = mysqlPassword
app.config['MYSQL_DB'] = mysqlDatabase
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

''' User Config Flags '''
# Log the Console messages on Terminal/Log File
# True : For Stdout/Terminal || False: For Log File
logFlag = False 

# +====================+ User Functions +====================+ #
"""
    Console Function
		Logs the Console messages on Terminal/Log File
		
    Parameters
    ----------
    buffStr : string
        The string which has to be printed or logged on the terminal (or in a log file).
		
    Returns
    -------
    None
"""
def console(buffStr):
	dateTime = datetime.datetime.now()
	queryBuff = ("{} | {}").format(dateTime, buffStr)
	if logFlag:
		with open('serviceLogs.log', 'a') as logger:
			logger.write(queryBuff+'\n')
	else:
		print(queryBuff)

		
"""
    Return Response Function
		Manipulate the response data in string or json format
		
    Parameters
    ----------
    command : string
        command request received from the browser/client
		
	command : string
        response regarding the command execution
		
	error : string
        error status (if Any), if not "None"
		
    Returns
    -------
	msgPayload : Json (or) String 
"""		
def returnResponse(command, response, error):
	msgPayload = {"command":command, "response":response, "error":error}
	return jsonify(msgPayload) # For Json Data
	#return str(msgPayload) # For String Data

"""
    Date Time Formatting Function
		Convert the Date Time ISOString to MySQL DateTime format (i.e YYYYMMDD HH:MM:SS)
		
    Parameters
    ----------
    ISOString : string
        ISO Format date time string data
		
    Returns
    -------
	formattedDateTime : String 
"""		
def dateTimeFormat(ISOString):
	year = ISOString[0:4]
	month = ISOString[4:6]
	day = ISOString[6:8]
	
	hour = ISOString[9:11]
	min = ISOString[11:13]
	sec = ISOString[13:15]
	formattedDateTime = (year+"-"+month+"-"+day+" "+hour+":"+min+":"+sec)
	return formattedDateTime

''' Flask Functions '''
@app.errorhandler(404) 
def invalid_route(e): 
    return "Invalid route."

@app.route("/")
def index():
	""" Present README documentation """
	# Open the README file
	with open(os.path.dirname(os.path.abspath(__file__)) + '/README.md', 'r') as markdown_file:
		# Read the content of the file
		content = markdown_file.read()
		# Convert to HTML
		return markdown.markdown(content), 200

@app.route("/devices/")
def devices():
	""" Get List of all devices registered """
	try:
		# Create Empty List
		deviceList = []
		# Connect MySQL Database
		cursor = mysql.connection.cursor()
		# Select all data from the Sql table
		cursor.execute("SELECT * FROM "+mysqlTable);
		listDevices = cursor.fetchall()
		# Close the MySQL Connection 
		cursor.close()
		# Get each device detail and append it into the list
		for device in listDevices:
			deviceDetails = {"deviceId":device["deviceid"],"deviceName":device["devicename"],"sensors":device["sensors"] }
			deviceList.append(deviceDetails)
		# Return the list of devices with their details
		return returnResponse("devices",deviceList,"none"), 200
	
	except Exception as error:
		console("[ FLASKLIST ] Error: "+str(error))
		# If any Error occured while performing above query send the error to client
		return returnResponse("devices","failed",str(error)), 409

@app.route("/addDevice")
def addDevice():
	try:
		# Extract the request arguments from the url
		deviceId = request.args.get('deviceId', None) 
		deviceName = request.args.get('deviceName', None) 
		preSenId = request.args.get('preSenId', None)
		tempSenId = request.args.get('tempSenId', None)
		
		# Create a formatted dictionary for sensors unique identifiers
		sensorDetails = {"temperature":tempSenId,"pressure":preSenId}
		# Connect MySQL Database
		cursor = mysql.connection.cursor()
		# Create a required SQL
		sqlQuery = ('INSERT INTO `devices`(`deviceid`, `devicename`, `sensors`) VALUES ("{}","{}","{}")').format(deviceId, deviceName, sensorDetails)
		# Execute query to insert the sensor details in devices table
		cursor.execute(sqlQuery)
		# Commit the mysql connection to perform/update changes
		mysql.connection.commit()
		
		# Check the response for the row count
		if cursor.rowcount == 1:
			console("[ FLASK ADD ] Added Device into the Database! DeviceId:"+str(deviceId))
		else:
			console("[ FLASK ADD ] Failed to Add Device into the Database! DeviceId:"+str(deviceId))
		
		# Create a required SQL
		sqlQuery = ('CREATE TABLE `{}`.`{}` ( `id` INT(10) NOT NULL AUTO_INCREMENT , `pressure` FLOAT(10) NOT NULL , `temperature` FLOAT(10) NOT NULL ,  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY  (`id`)) ENGINE = InnoDB').format(mysqlDatabase, deviceId)
		# Execute query to to create a table with the unique device identifiers
		cursor.execute(sqlQuery)
		# Commit the mysql connection to perform/update changes
		mysql.connection.commit()
		# Close the MySQL Connection
		cursor.close()
		console("[ FLASK ADD ] Created Table for the DeviceId:"+str(deviceId))
		# Return the added new device identifier
		return returnResponse("addDevice",deviceId,"none"), 200
		
	except Exception as error:
		console("[ FLASK ADD ] Error: "+str(error))
		# If any Error occured while performing above query send the error to client
		return returnResponse("addDevice","failed",str(error)), 409

		
@app.route("/updateDevice")
def updateDevice():
	try:
		# Extract the request arguments from the url
		deviceId = request.args.get('deviceId', None) 
		newDeviceName = request.args.get('newDeviceName', None) 
		
		# Connect MySQL Database
		cursor = mysql.connection.cursor()	
		# Create a required SQL
		sqlQuery = ("UPDATE `devices` SET `devicename` = '{}' WHERE `deviceid` = '{}'").format(newDeviceName, deviceId)
		# Execute query to update the device name
		cursor.execute(sqlQuery)
		# Commit the mysql connection to perform/update changes
		mysql.connection.commit()

		# Check the response for the row count
		if cursor.rowcount == 1:
			console("[ FLASKUPDT ] Updated Device Name into the Database! DeviceId:"+str(deviceId))
		else:
			console("[ FLASKUPDT ] Failed to Update Device Name into the Database! DeviceId:"+str(deviceId))
		# Close the MySQL Connection
		cursor.close()
		# Return the updated device identifier
		return returnResponse("updateDevice",deviceId,"none"), 200
	except Exception as error:
		console("[ FLASKUPDT ] Error: "+str(error))
		# If any Error occured while performing above query send the error to client
		return returnResponse("updateDevice","failed",str(error)), 404

@app.route("/deviceData")
def deviceData():
	try:
		# Extract the request arguments from the url
		deviceId = request.args.get('deviceId', None) 
		presValue = request.args.get('presValue', None) 
		tempValue = request.args.get('tempValue', None)
		
		# Connect MySQL Database
		cursor = mysql.connection.cursor()	
		# Create a required SQL
		sqlQuery = ('INSERT INTO `{}`(`temperature`, `pressure`) VALUES ({},{})').format(deviceId, tempValue, presValue)
		# Execute query to insert the sensor data values its device id table
		cursor.execute(sqlQuery)
		# Commit the mysql connection to perform/update changes
		mysql.connection.commit()

		# Check the response for the row count
		if cursor.rowcount == 1:
			console("[ FLASKDATA ] Data Saved to the Database! DeviceId:"+str(deviceId))
		else:
			console("[ FLASKDATA ] Unable to Save Data to the Database! DeviceId:"+str(deviceId))
		# Close the MySQL Connection
		cursor.close()
		# Return the saved sensor value device identifier
		return returnResponse("deviceData",deviceId,"none"), 200
		
	except Exception as error:
		console("[ FLASKDATA ] Error: "+str(error))
		# If any Error occured while performing above query send the error to client
		return returnResponse("deviceData","failed",str(error)), 409
	

@app.route("/getData")
def getDeviceData():
	try:
		# Extract the request arguments from the url
		deviceId = request.args.get('deviceId', None) 
		startTime = request.args.get('startTime', None) 
		endTime = request.args.get('endTime', None)
		
		# Connect MySQL Database
		cursor = mysql.connection.cursor()
		# Create a required SQL
		sqlQuery = ("SELECT * FROM `{}` WHERE timestamp BETWEEN '{}' AND '{}'").format(deviceId, dateTimeFormat(startTime), dateTimeFormat(endTime))
		# Execute query to get the sensor data values from the selected start and stop timestamop
		cursor.execute(sqlQuery)
		# Get all data requested from the Sql table
		listData = cursor.fetchall()
		# Close the MySQL Connection
		cursor.close()
		# Return the list of sensor data
		return returnResponse("getData",listData,"none"), 200
		
	except Exception as error:
		console("[ FLASKDATA ] Error: "+str(error))
		# If any Error occured while performing above query send the error to client
		return returnResponse("getData","failed",str(error)), 409
		
''' System Function Call '''
if  __name__ == '__main__': 
	console(" +=============== Service Started ===============+ ")
	try:
		# Run the Flask Application 
		app.run(debug=False)
			
	# Exception Handeling (if Any)
	except Exception as error:
		console("[  EXCPTIN  ] Error : "+str(error))
		# Exit the Script
		sys.exit()

	# Check KeyboardInterrupt to Terminate Script
	except KeyboardInterrupt:
		console("[ USER INTT ] User Interrupt Recieved!")
		console("[ USER INTT ] Terminating Server!")
		console(" +=============== Service Stopped ===============+ ")
		# Exit the Script
		sys.exit()
		
		
''' Nothing To See Here '''