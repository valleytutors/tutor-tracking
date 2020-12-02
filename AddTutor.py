import gspread
from notion.client import NotionClient
import gspread_formatting
import config

#NotionClient initializations
client = NotionClient(token_v2=config.NOTION_AUTH_TOKEN)
page = client.get_block(config.NOTION_TUTOR_PAGE)
cv = client.get_collection_view(config.NOTION_TUTOR_PAGE)

#gspread initializations
gc = gspread.oauth()
sh = gc.open_by_url(config.TUTOR_SPREADSHEET_URL)
sheet1 = sh.get_worksheet(0)
ws = sheet1.get_all_values()
#Enter the row range to add to notion

print("To add a range of Tutors to the Notion Database, enter the row number range below.\n\nIf the row is highlighted:\n\n[RED] - Past responses that are incompatible with this program.\n\n[GREEN] - Responses that have already been added to the database using this program.\n\n[NO COLOR] - Responses that have not been added to the database yet. These are the ones you are looking to add.\n")

print("Array Size: " + str(len(ws)) + " down by " + str(len(ws[0])) + " across")

begin = input("Enter the number of start row: ")
end = input("Enter the number of the end row: ")


#Tests to make sure that the inputs for begin and end are numbers greater than 0
if begin.isnumeric() == False or end.isnumeric() == False or int(begin) < 1 or int(end) < 1:
	print("Please enter a number greater than 0 for both fields")
	quit()

#Creates list with all the row numbers expected to parse through
sheetRange = []
n = 0
while int(begin) + n <= int(end):
	sheetRange.append(int(begin) + n)
	n += 1
#Confirmation phase

print("\nWould you like to add the following " + str(len(sheetRange)) + " Tutors to the Notion database?\n")
numTutors = 0

for y in sheetRange:
	print(str(y) + ": " + ws[y-1][2])
	numTutors += 1

print("\n")
confirmation = input("#################\n# [Y]: Continue #\n# [N]: Cancel   #\n#################\n\nYour answer: ")


if confirmation != "N" and confirmation != "Y" and confirmation != "n" and confirmation != "y":
	print("Not Y or N, exiting")
	quit()

if confirmation == "N" or confirmation == "n":
	print("Process canceled")
	quit()

baseBGColor = "backgroundColor=(red=0.85490197;green=0.9411765;blue=0.83137256);backgroundColorStyle=(rgbColor=(red=0.85490197;green=0.9411765;blue=0.83137256))" #String result of red background color on Gsheets

numDuplicates = 0 
dummy = 1 #Dummy variable to fill for if statement... I know theres a way easier way but I learned it after making this and now i don't care...

#Parses through the rows and adds each tutor with their respective attributes
print("\nAdding tutors... Give me a sec, I need to concentrate...\n")
for x in sheetRange:

	a = x-1
#Checks if entry already exists by cross checking the color in sheets
	if str(gspread_formatting.get_user_entered_format(sheet1, "B" + str(x))) == baseBGColor:
		parthiv = input("\n" + ws[a][2] + " has already been added to Notion. Would you like to add anyway? [Y/N]: ")
		if parthiv == "Y" or parthiv == "y":
			dummy = 2
		elif parthiv == "N" or parthiv == "n":
			print("Ok, " + ws[a][2] + " has been skipped")
			numDuplicates += 1
			numTutors -= 1	
			continue
		else:
			print("Do you not know how to read? Y or N, buddy... To be safe, I am not adding " + ws[a][2])
			numDuplicates += 1
			numTutors -= 1	
			continue


	row = cv.collection.add_row()
	row.Name = ws[x-1][2]
	grade = ""
	if ws[a][3] == "Freshman":
		grade = "9th"
	elif ws[a][3] == "Sophomore":
		grade = "10th"
	elif ws[a][3] == "Junior":
		grade = "11th"
	elif ws[a][3] =="Senior":
		grade = "12th"
	elif ws[a][3] == "Other":
		grade = "Other"
	row.Grade_Level = grade
	row.Notes = ws[a][20]
	row.Subjects = ws[a][4].split(", ")
	row.Available_Days = ws[a][19].split(", ")
	row.Available_Time = ws[a][10]
	row.Maximum_Tutees = int(ws[a][18])
	row.Discord_ID = ws[a][11]
	row.Phone = ws[a][13]
	row.Email = ws[a][1]
	
	sh.get_worksheet(0).format("A" + str(x) + ":AA" + str(x), {\
		"backgroundColor": {\
			"red": 38.0,
			"green": 16.0,
			"blue": 44.0\
		}})

	duplicates = []
print("\n" + str(numDuplicates) + " duplicate(s) were found and have not been added to Notion.")
print(str(numTutors) + " tutors have been successfully added to the Notion Database. Enjoy!")
