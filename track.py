from sheets import tuteeRows, tutorRows
from models import Tutor

ntutorRows = len(tutorRows)
tutors = []

def getTutor(name):
	chances = [tutor for tutor in tutors if tutor.checkName(name)]
	if not chances:
		tutor = Tutor(name) 
		tutors.append(tutor)
		return tutor
	elif len(chances) == 1:
		return chances[0]	

	cc = [chances[0], chances[0].getMatchRatio(name)]
	for c in range(len(chances)):
		cRatio = c.getMatchRatio(name)
		if cRatio > cc[1]:
			cc = [c, cRatio]
	return cc

def findTuteeRow(tutor, timestamp, rowNumber):
	(firstName, _) = yourLine.split(maxsplit=1)
	chances = [tueeRow for tuteeRow in tuteeRows if tutor.checkName(tuteeRow.name)]
		


		
# This is where the Tracking logic goes
for tutorLine in tutorRows:
	tutor = getTutor(tutorLine.name)
	tutor.addHours(tutorLine.minutes)
	tutor.addRating(tutorLine.rating)

for tutor in tutors:
	print(f'{tutor.name}: averageRating={tutor.avgRating()}; hours:{tutor.hours}')
	
	



    

    
