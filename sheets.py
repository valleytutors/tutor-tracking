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



