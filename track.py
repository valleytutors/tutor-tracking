from utils import getMatchRatio, checkName, checkInName
from sheets import tuteeRows, tutorRows
from models import Tutor
import config
from datetime import datetime
import sys

def getTutor(name):
	chances = [tutor for tutor in tutors \
		if checkName(tutor.name, name)]
	if not chances:
		tutor = Tutor(name) 
		tutors.append(tutor)
		return tutor
	elif len(chances) == 1:
		return chances[0]	

	cc = (None, 0)
	for chance in chances:
		cRatio = getMatchRatio(chance.name, name)
		if cRatio > cc[1]:
			cc = (chance, cRatio)
	return cc[0]

def findTuteeRow(tutor, entry):
	# returns a tuple (boolean, tuteeRow)
	# boolean - confirmation that the tuteeRow is correct
	#	If it's false, it could still be right, but not confirmed
	#	Confirmation happens through the date field(added recently)
	#	Or the timestamp fields have to be within a certain time
	#	of each other(config.NEEDED_TIMESTAMP_DIFF)
	(entryCount, entry) = entry
	allChances = [tuteeRow for tuteeRow in tuteeRows \
		if checkInName(tutor.name, tuteeRow.tutor) and \
		checkInName(tuteeRow.name, entry.tutee)]
	if not allChances:
		return (False, None)

	timestamp = lambda t: datetime.strptime(t, \
		"%m/%d/%Y %H:%M:%S") 
	tutorTimestamp = timestamp(entry.timestamp)
	delta = lambda t: abs((timestamp(t) - tutorTimestamp).days)

	cc = (None, float('inf'))
	for chance in allChances:
		# If theres a date we are done rest of the logic is not needed
		if entry.date:
			if entry.date == chance.date:
				return (True, chance)
		d = delta(chance.timestamp)
		if d <= cc[1]:
			cc = (chance, d)

	(cc, _) = cc
	cdelta = delta(cc.timestamp)
	if cdelta < config.NEEDED_TIMESTAMP_DIFF:
		return (True, cc)
	else:
		return (False, cc)


def getRowInput():
	i = input(f'Enter a number from 1-{len(tuteeRows)} or y/n: ')
	i = i.lower()
	if i.isdigit():
		return (False, tuteeRows[int(i)-1])
	else:
		return (('n' not in i.lower()), None)
		

def tryToConfirm(tuteeRow, tutorRow):
	rowInfo = lambda: print(f'{tutorRow.timestamp}= tutor: {tutorRow.name}; tutee: {tutorRow.tutee}')
	countHours = False
	if not tuteeRow:
		print()
		print("=====MISSING ENTRY=====") 
		print("There are no tutee form entries for:")
		rowInfo()
		print("Please enter a row number if you can find the matching tutee form entry")
		print("Otherwise just confirm if the hours should count and enter 'n' if they shouldn't count")
		(c, tuteeRow) = getRowInput()
		if c:
			countHours = True
	else:
		print()
		print("=====CONFIRMATION NEEDED=====")
		print(f"I found a possible tutee form entry for:")
		rowInfo()
		print("--RAW TUTEE FORM ENTRY DATA--") 
		print(", ".join(tuteeRow.rawRow))
		print("--RAW DATA END--")
		print()
		print("Please check if this is the right entry and just hit enter if it is")
		print("If it's wrong please try and find the right row number and enter that")
		print("If it's wrong and there is no row entry, enter 'n'")
		(c, tRow) = getRowInput()
		if tRow:
			tuteeRow = tRow
		else:
			if not c:
				print("Since there is no form entry, should the hours still count? ")
				i = input("type n if they shouldn't: ")
				if 'n' not in i.lower():
					countHours = True
	
	return (countHours, tuteeRow)

def confirmHours(tutor, tutorRow, tuteeRow):
	strikes = 0
	if not tutorRow.completion:
		strikes += 3
	if not tuteeRow.completion:
		strikes += 1
	rating = tuteeRow.rating
	if rating < 4:
		strikes += 4-rating
	if strikes > 3:
		return False
	return True

def trackTutors():
	tutors = []

	
	print("I am about to start loading in tutee form entries into each tutor")
	print("There might be issues with confirming tutee entries")
	print("If something comes up you will be asked to find and enter row numbers or just confirm hours since tutee form entries aren't necessary but helpful")
	print("Keep in mind that the default is trusting tutors, so instead whenever you are asked to enter y/n, you can just hit enter and 'yes' will be assumed")
	print("You can try and edit the spreadsheet and restart if it's just a serious spelling error")
	print("But the program can usually deal with most spelling errors")
	
	# This is where the Tracking logic goes
	for tutorRow in tutorRows:
		tutor = getTutor(tutorRow.name)
		tutorEntry = tutor.addTutorEntry(tutorRow)
		(confirmed, tuteeRow) = findTuteeRow(tutor, tutorEntry)
		countHours = False
	
		if not confirmed:
			(countHours, tuteeRow) = tryToConfirm(tuteeRow, tutorRow)
	
	
		if countHours:
			tutor.addHours(tutorRow.length)
			if tuteeRow:
				tutor.addTuteeEntry(tuteeRow)
		else:
			if tuteeRow:
				if confirmHours(tutor, tutorRow, tuteeRow):
					tutor.addTuteeEntry(tuteeRow)
					tutor.addHours(tutorRow.length)
				else:
					tutor.addTuteeEntry(tuteeRow)
