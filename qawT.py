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

import sys
import os
import argparse

from qawlibs import qaexceptions,qabackend

class QAWTerminalSession:
	
	loadedSets = []
	qaBackend = qabackend.QABackend()

	def __init__(self):
		parser = argparse.ArgumentParser(description='QAW: Questions & Answers Weighted (get them right and they show up less)')
		parser.add_argument('-s','--show-sets',help='List existing QA sets',action='store_true')
		parser.add_argument('-d','--drop-sets',help='Delete QA sets (<set1>:<set2>:...:<setn>)')
		parser.add_argument('-l','--load-sets',help='Load existing sets.  (i.e. <set1>:<set2>:...:<setn>)')
		parser.add_argument('-a','--add-sets',help='Load question/answer sets from text files. (<file1>:<file2>:...:<filen>)')
		
		self.args = vars(parser.parse_args())	

		if self.args['show_sets']:
			self._showSets()

		if self.args['add_sets'] != None:
			for qaSetFile in self.args['add_sets'].split(":"):
				print "Adding sets from "+qaSetFile
				print "Enter QA Set Name (existing to append):"
				name = raw_input()
				print self.qaBackend.loadTextFile(qaSetFile,name)
		
		if self.args['drop_sets'] != None:
			for qaSet in self.args['drop_sets'].split(":"):
				print self.qaBackend.dropTable(qaSet)	

		if self.args['load_sets'] != None:
			self._loadSets(self.args['load_sets'].split(":"))
		else:
			self._loadSets()

	def _loadSets(self,sets=list()):
		for qaSet in sets:
			if qaSet in self.qaBackend.loadCurrentTables() and len(qaSet.rstrip()) > 0:
                		self.loadedSets.append(qaSet)
		if len(self.loadedSets) < 1:
			self._addAnotherSet()
		else:
                	print "Start session?  (y/n)"
                	keyAnswer = raw_input()
                	while keyAnswer.lower() != 'y':
                		if keyAnswer.lower() != 'n':
                            		print "Sorry, you must choose y or n."
                                	keyAnswer = raw_input()
                        	else:
                           		self._addAnotherSet()
                                	keyAnswer = raw_input()

                	self._qaSessionStart()
		
	
	def _showSets(self):
		print "Available QA Sets :"
		if len(self.loadedSets) < 1:
			for qaSet in self.qaBackend.loadCurrentTables():
                        	print "* "+qaSet
		else:
			self._showLoadedSets()
			for qaSet in self.qaBackend.loadCurrentTables():
				if qaSet not in self.loadedSets:
					print "* "+qaSet

	def _showLoadedSets(self):
		print "Loaded QA Sets :"
		for qaSet in self.loadedSets:
			print qaSet

	def _addAnotherSet(self):
		self._showSets()
		print "Please enter sets separted by colon (set1:set2:...:setn)  [q to exit]"
		setsEntered = raw_input()
		if setsEntered != 'q':
			self._loadSets(setsEntered.split(":"))

	def _qaSessionStart(self):
		stillRunning = True
                
		QAFromTable = ""
		QAQuestionID = 0

		while stillRunning:
			os.system(['clear','cls'][os.name=='nt'])
			try:
				QA = self.qaBackend.loadQuestionAnswer(self.loadedSets)
				
				if QA != None and QA[1] != None:

					if (QAFromTable == QA[0] and QAQuestionID != QA[1][0]) or QAFromTable != QA[0]:

						QAFromTable = QA[0]
						QAQuestionID = QA[1][0]
						Q = QA[1][1]
						A = QA[1][2]
						QAConfidence = QA[1][3]

						print "[press (q) to end session]    Q from set: "+QAFromTable+" confidence rating:"+str(QAConfidence)
						print ""
						print Q

						print "\n(Any key to show answer....)"
						keyAnswer = raw_input()
						if keyAnswer.lower() == 'q':
							stillRunning = False
							break

						print "  =>  "+A
			
						print "\nWere you right? (y/n)"
						while True:
							keyAnswer = raw_input()
							keyAnswer = keyAnswer.lower()
							if keyAnswer == 'q':
								stillRunning = False
								break
							elif keyAnswer == 'y':
								self.qaBackend.updateConfidenceLevel(QAFromTable,QAQuestionID,QAConfidence+5)
								break
							elif keyAnswer == 'n':
                        	                	        self.qaBackend.updateConfidenceLevel(QAFromTable,QAQuestionID,QAConfidence-5)
								break
			except qaexceptions.QuestionFetchError, e:
				print e
	
startATextSession = QAWTerminalSession()
