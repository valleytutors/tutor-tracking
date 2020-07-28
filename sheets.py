import csv
import gspread
import config
from models import TutorRow, TuteeRow 

client = gspread.oauth()


tutorSH = client.open_by_url(config.TUTOR_SPREADSHEET_URL)
tuteeSH = client.open_by_url(config.TUTEE_SPREADSHEET_URL) 

tutorForm = tutorSH.get_worksheet(0).get_all_values()
tuteeForm = tuteeSH.get_worksheet(0).get_all_values()

tutorSHHeaders = tutorForm[0]
tuteeSHHeaders = tuteeForm[0]

tutorIndexes = {}
for value, header in config.TUTOR_HEADERS.items():
	tutorIndexes[value] = tutorSHHeaders.index(header)

tuteeIndexes = {}
for value, header in config.TUTEE_HEADERS.items():
	tuteeIndexes[value] = tuteeSHHeaders.index(header)

#class TutorIndexes:
#	name = tutorHeaders.index("Name")
#	tutee = tutorHeaders.index("Who did you tutor?")
#	minutes = tutorHeaders.index("How long was the tutoring session")
#	rating = tutorHeaders.index("How would you rate your tutee(s)?")
#	completion = tutorHeaders.index("Check this box to verify you had your meeting")
#	timestamp = tutorHeaders.index("Timestamp")
#
#class TuteeIndexes:
#	name = tuteeHeaders.index("Student's Name")
#	tutor = tuteeHeaders.index("Tutor(s)' Name")
#	minutes = tuteeHeaders.index("How long was your session?")
#	rating = tuteeHeaders.index("How would you rate your tutor(s)")
#	completion = tuteeHeaders.index("Check the box to verify the session was completed")
#	timestamp = tuteeHeaders.index("Timestamp")
#	wentWell = tuteeHeaders.index("What went well?")
#	wentPoorly = tuteeHeaders.index("What went poorly?")
#

tutorRows = []
TutorRow.indexes = tutorIndexes
# print("Loading Tutors")
for i in range(1, len(tutorForm)):
	rowRaw = tutorForm[i]
	row = TutorRow(rowRaw, i)
	tutorRows.append(row)
	# print(f'Loaded an entry for {row.name} filled at {rowRaw[0]}')

tuteeRows = []
TuteeRow.indexes = tuteeIndexes
# print("Loading Tutees")
for i in range(1, len(tuteeForm)):
	rowRaw = tuteeForm[i]
	row = TuteeRow(rowRaw, i)
	tuteeRows.append(row)
	# print(f'Loaded an entry for {row.name} filled at {rowRaw[0]}')



