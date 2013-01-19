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

class ParsingError(Exception):
	def __init__(self,lineCount):
		self.msg = "Question/Answer parsing failed on line: "+str(lineCount)
	def __str__(self):
		return self.msg

class QuestionFetchError(Exception):
	def __init__(self):
		self.msg = "Failed QA request."
	def __str__(self):
		return self.msg
