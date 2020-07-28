from difflib import SequenceMatcher

NEEDED_RATIO = .95

class Tutor:
	def __init__(self, name):
		self.name = name
		# Hours refers to the time volunteered and is in hours
		self.hours = 0
		self.ratings = []

	def addHours(self, hours, inMinutes=True):
	    # The spreadsheet is in minutes so thats the default 
		if inMinutes:
			self.hours += hours/60
		else:
			self.hours += hours
    	
	def addRating(self, rating):
		self.ratings.append(rating)

	def avgRating(self, ):
		return sum(self.ratings)/len(self.ratings)
	
	def getMatchRatio(self, name):
		matcher = SequenceMatcher(None, self.name, name)
		return matcher.ratio()

	def checkName(self, name):
		if self.name.lower() == name.lower():
			return True
		elif self.getMatchRatio(name) > NEEDED_RATIO:
			return True

		return False

class TutorRow:
	indexes = {}
	def __init__(self, row, rowNumber):
		c = TutorRow.indexes
		self.name = row[c['name']]
		self.tutee = row[c['tutee']]
		self.minutes = int(row[c['minutes']])
		self.rating = int(row[c['rating']])
		self.completion = row[c['completion']] == "Meeting Was Completed"
		self.timestamp = row[c['timestamp']]
		self.rowNumber = rowNumber

class TuteeRow:
	indexes = {}
	def __init__(self, row, rowNumber):
		c = TuteeRow.indexes
		self.name = row[c['name']]
		self.tutor = row[c['tutor']]
		self.minutes = row[c['minutes']]
		self.rating = row[c['rating']]
		self.completion = row[c['completion']] == "The meeting was completed"
		self.timestamp = row[c['timestamp']]
		self.rowNumber = rowNumber

