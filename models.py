class TutorRow:
	indexes = {}
	def __init__(self, row, rowNumber):
		c = TutorRow.indexes
		self.rawRow = row
		self.name = row[c['name']]
		self.tutee = row[c['tutee']]
		self.length = int(row[c['length']])
		self.rating = int(row[c['rating']])
		self.completion = row[c['completion']] == "Meeting Was Completed"
		self.timestamp = row[c['timestamp']]
		self.date = row[c['date']]
		self.rowNumber = rowNumber
	
	def __str__(self):
		return str(self.rawRow)

class TuteeRow:
	indexes = {}
	def __init__(self, row, rowNumber):
		c = TuteeRow.indexes
		self.rawRow = row
		self.name = row[c['name']]
		self.tutor = row[c['tutor']]
		self.length = row[c['length']]
		self.rating = int(row[c['rating']])
		self.completion = row[c['completion']] == "The meeting was completed"
		self.timestamp = row[c['timestamp']]
		self.date = row[c['date']]
		self.rowNumber = rowNumber
	
	def __str__(self):
		return str(self.rawRow)

class Tutor:
	def __init__(self, name):
		self.name = name
		# Hours refers to the time volunteered and is in hours
		self.hours = 0
		# Number of entries in tutor spreadsheet
		self.count = 0
		# List of tuples
		# (count, rowEntry)
		self.tutorEntries = []
		self.tuteeEntries = []
	
	def addTutorEntry(self, row: TutorRow):
		centry = (self.count, row)
		self.tutorEntries.append(centry)
		self.count += 1
		return centry

	def addTuteeEntry(self, row: TuteeRow):
		self.tuteeEntries.append(row)
		return row

	def addHours(self, hours, inMinutes=True):
	    # The spreadsheet is in minutes so thats the default 
		if inMinutes:
			self.hours += hours/60
		else:
			self.hours += hours

	def avgRating(self):
		ratings = [entry.rating for entry in self.tuteeEntries]
		return sum(ratings)/len(self.ratings)



