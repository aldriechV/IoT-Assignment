from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta
import time

DBName = "test" #Use this to change which Database we're accessing
connectionURL = "mongodb+srv://kylado:Ilovececs327@cluster0.06rwogu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" #Put your database URL here
sensorTable = "Traffic Data" #Change this to the name of your sensor data table

def QueryToList(query):
  return list(query)
  #HINT: MongoDB queries are iterable

def QueryDatabase() -> []:
	global DBName
	global connectionURL
	global currentDBName
	global running
	global filterTime
	global sensorTable
	cluster = None
	client = None
	db = None
	try:
		cluster = connectionURL
		client = MongoClient(cluster)
		db = client[DBName]
		print("Database collections: ", db.list_collection_names())

		#We first ask the user which collection they'd like to draw from.
		sensorTable = db[sensorTable]
		print("Table:", sensorTable)
		#We convert the cursor that mongo gives us to a list for easier iteration.
		timeCutOff = datetime.now() - timedelta(minutes=0) #TODO: Set how many minutes you allow

		oldDocuments = QueryToList(sensorTable.find({"time":{"$gte":timeCutOff}}))
		currentDocuments = QueryToList(sensorTable.find({"time":{"$lte":timeCutOff}}))

		print("Current Docs:",currentDocuments)
		print("Old Docs:",oldDocuments)

		#TODO: Parse the documents that you get back for the sensor data that you need
		#Return that sensor data as a list
		return currentDocuments


	except Exception as e:
		print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		exit(0)

