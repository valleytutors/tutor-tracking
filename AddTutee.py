import gspread
from notion.client import NotionClient
import gspread_formatting
import config

#NotionClient initializations
client = NotionClient(token_v2=config.NOTION_AUTH_TOKEN)
page = client.get_block(config.NOTION_TUTEE_PAGE)
cv = client.get_collection_view(config.NOTION_TUTEE_PAGE)

#gspread initializations
gc = gspread.oauth()
sh = gc.open_by_url(config.TUTEE_SPREADSHEET_URL)
sheet1 = sh.get_worksheet(0)
ws = sheet1.get_all_values()
#Enter the row range to add to notion

print("To add a range of Tutees to the Notion Database, enter the row number range below.\n\nIf the row is highlighted:\n\n[RED] - Past responses that are incompatible with this program (There aren't actually any of these for Tutees).\n\n[GREEN] - Responses that have already been added to the database using this program.\n\n[NO COLOR] - Responses that have not been added to the database yet. These are the ones you are looking to add.\n")

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

print("Would you like to add the following " + str(len(sheetRange)) + " Tutees to the Notion database?\n")
numTutees = 0
for y in sheetRange:
	print(str(y) + ": " + ws[y-1][2])
	numTutees += 1

print("\n")
confirmation = input("#################\n# [Y]: Continue #\n# [N]: Cancel   #\n#################\n\nYour answer: ")


if confirmation != "N" and confirmation != "Y":
	print("Not Y or N, exiting")
	quit()

if confirmation == "N":
	print("Process canceled")

#Parses through the rows and adds each tutee with their respective attributes

baseBGColor = "backgroundColor=(red=0.85490197;green=0.9411765;blue=0.83137256);backgroundColorStyle=(rgbColor=(red=0.85490197;green=0.9411765;blue=0.83137256))"
numDuplicates = 0
dummy = 1

print("\nAdding Tutees... Give me a sec, I need to concentrate...\n")
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
			numTutees -= 1	
			continue
		else:
			print("Do you not know how to read? Y or N, buddy... To be safe, I am not adding " + ws[a][2])
			numDuplicates += 1
			numTutees -= 1	
			continue

	if confirmation == "N": #For testing purposes only
		break

	row = cv.collection.add_row()

	row.Name = ws[a][2]
	row.Status = "Available (Form filled)"
	row.Subjects = ws[a][8].split(", ")
	row.Available_Time = ws[a][6]
	row.Communication_Type = ["Email"]
	row.Communication_Info = ws[a][1]
	row.Grade = ws[a][5]
	row.Notes = ws[a][9]
	row.Additional_Notes = ws[a][12]
	row.Parent = ws[a][3]
	row.Available_Days = ws[a][7].split(", ")
	row.School = ws[a][4]
	
#Color in the Google Sheet Response Form

	sh.get_worksheet(0).format("A" + str(x) + ":AA" + str(x), {\
		"backgroundColor": {\
			"red": 38.0,
			"green": 16.0,
			"blue": 44.0\
		}})
print("\n" + str(numDuplicates) + " duplicate(s) were found and have not been added to Notion.")
print(str(numTutees) + " tutees have been successfully added to the Notion Database. Enjoy!")
