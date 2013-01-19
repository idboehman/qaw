#!/usr/bin/python

'''  
    Morgan Phillips (c) 2013

    This file is part of qaw.

    qaw is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    qaw is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with qaw.  If not, see <http://www.gnu.org/licenses/>.
'''

import sqlite3
import random
import re

import qaexceptions

class QABackend:
	
	dbConn = sqlite3.connect('qaw.db')

	def updateConfidenceLevel(self,tableName,questionID,newConfidence):
		
		if(int(newConfidence) < 0):
			newConfidence = 0
		elif(int(newConfidence) > 100):
			newConfidence = 100

		dbCursor = self.dbConn.cursor()
		
		updateConfidenceSQL = "UPDATE "+tableName+" SET confidence='"
		updateConfidenceSQL += str(newConfidence)+"' WHERE "
		updateConfidenceSQL += "id='"+str(questionID)+"'"
		
		return dbCursor.execute(updateConfidenceSQL)

	def loadCurrentTables(self):
		dbCursor = self.dbConn.cursor()
		
		loadTablesSQL = "SELECT name FROM sqlite_master WHERE type='table'"			
		
		returnList = list()
		for tableName in dbCursor.execute(loadTablesSQL):
			if tableName[0] != "sqlite_sequence":
				returnList.append(tableName[0])			
		
		return returnList

	def loadQuestionAnswer(self,tableNames = list()):
		dbCursor = self.dbConn.cursor()
		
		getQuestionAnswerSQL = "SELECT * FROM "
		
		returnList = list()
		tableName = random.choice(tableNames)
		returnList.append(tableName)

		getQuestionAnswerSQL += tableName
		
		confidenceLevel = random.randint(0,100)
		getQuestionAnswerSQL += " WHERE confidence < "+str(confidenceLevel)
		getQuestionAnswerSQL += " ORDER BY RANDOM() LIMIT 1"

		dbCursor.execute(getQuestionAnswerSQL)
		
		returnList.append(dbCursor.fetchone())
		
		return returnList
	
	def loadTextFile(self,textFile,tableName=None):
			try:
				fileHandle = open(textFile,'r')
				
				#A default tableName appears....
				if tableName == None:
					tableName = textFile.split('/')[-1].replace('.','')
				
				dbCursor = self.dbConn.cursor()
				
				createTableIfSQL = "CREATE TABLE IF NOT EXISTS "+tableName
				createTableIfSQL += " (id INTEGER PRIMARY KEY AUTOINCREMENT,"
				createTableIfSQL += "question TEXT UNIQUE,"
				createTableIfSQL += "answer TEXT,confidence INTEGER DEFAULT 0)"

				dbCursor.execute(createTableIfSQL)
	
				lineCount = 0
				for line in fileHandle:
					lineCount += 1
					
					match = re.search("[.*,.*].*",line)
					if match != None:
						try:
							QA = eval(line)	
							insertSQL = "INSERT INTO "+tableName
							insertSQL += " (question,answer) VALUES ('"+QA[0]+"','"+QA[1]+"')"
				
							dbCursor.execute(insertSQL)
					
						except:
							print qaexceptions.ParsingError(lineCount)	
	
				self.dbConn.commit()
				return "Finished"
			
			except IOError, e:
				return e

	def dropTable(self,tableName):
		try:

			dbCursor = self.dbConn.cursor()
								   
			dropTableIfSQL = "DROP TABLE IF EXISTS "
			dropTableIfSQL += tableName
	
			dbCursor.execute(dropTableIfSQL)
			
			return "Dropped: "+tableName
		except:
			return "Failed to drop: "+tableName
