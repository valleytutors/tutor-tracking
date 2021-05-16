from utils import getMatchRatio, \
    checkName, checkInName, checkOne
from sheets import tuteeForm, tutorForm, \
    tutorIndexes, tuteeIndexes
import sheets
from models import Tutor, TutorRow, TuteeRow
from remote import lastRow
import config
from datetime import datetime
import sys

tutors = []

tutorRows = []

startRow = int(input("What row to start tracking from(enter exact row number in spreadsheet)? "))
# print("Loading Tutors")
for i in range(startRow, len(tutorForm)):
    rowRaw = tutorForm[i]
    if not rowRaw[0]:
        continue
    row = TutorRow(rowRaw, i, tutorIndexes)
    tutorRows.append(row)
    # print(f'Loaded an entry for {row.name} filled at {rowRaw[0]}')

tuteeRows = []
# print("Loading Tutees")
for i in range(1, len(tuteeForm)):
    rowRaw = tuteeForm[i]
    if not rowRaw[0]:
        continue
    row = TuteeRow(rowRaw, i, tuteeIndexes)
    tuteeRows.append(row)
    # print(f'Loaded an entry for {row.name} filled at {rowRaw[0]}')

def getTutor(name):
    chances = [tutor for tutor in tutors \
                if checkInName(tutor.name, name)]

    if not chances:
        try:
            tutor = Tutor(name) 
        except NameError:
            return None
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
    #   If it's false, it could still be right, but not confirmed
    #   Confirmation happens through the date field(added recently)
    #   Or the timestamp fields have to be within a certain time
    #   of each other(config.NEEDED_TIMESTAMP_DIFF)
    (entryCount, entry) = entry
    allChances = [tuteeRow for tuteeRow in tuteeRows \
        if checkOne(tutor.name.split()[0], tuteeRow.tutor) and \
        checkOne(tuteeRow.name.split()[0], entry.tutee)]
    if not allChances:
        return None

    timestamp = lambda t: datetime.strptime(t, \
        "%m/%d/%Y %H:%M:%S") 
    tutorTimestamp = timestamp(entry.timestamp)
    delta = lambda t: abs((timestamp(t) - tutorTimestamp).days)

    cc = (None, float('inf'))
    for chance in allChances:
        # If theres a date we are done rest of the logic is not needed
        if entry.date:
            if entry.date == chance.date:
                return chance
        d = delta(chance.timestamp)
        if d <= cc[1]:
            cc = (chance, d)

    (cc, _) = cc
    cdelta = delta(cc.timestamp)
    if cdelta < config.NEEDED_TIMESTAMP_DIFF:
        return cc
    else:
        return None


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
    resultTutee = None
    if not tuteeRow:
        print()
        print("=====MISSING ENTRY=====") 
        print("There are no tutee form entries for:")
        rowInfo()
        print("Please enter a row number if you can find the matching tutee form entry")
        print("Otherwise just confirm if the hours should count and enter 'n' if they shouldn't count")
        (c, resultTutee) = getRowInput()
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
            resultTutee = tuteeRow
        else:
            if c:
                resultTutee = tuteeRow
            else:
                print("Since there is no form entry, should the hours still count? ")
                i = input("type n if they shouldn't: ")
                if 'n' not in i.lower():
                    countHours = True
    
    return (countHours, tuteeRow)

def confirmHours(tutor, tutorRow, tuteeRow):
    # Possible check for duplicates here
    if not tutorRow.completion:
        return False
    if not tuteeRow:
        return True
    if tuteeRow.completion or tuteeRow.rating > 3:
        return True

    return False

def trackTutors():
    
    print("SETUP COMPLETED, LOADING TUTOR INFORMATION")
    # print("There might be issues with confirming tutee entries")
    # print("If something comes up you will be asked to find and enter row numbers or just confirm hours since tutee form entries aren't necessary but helpful")
    # print("Keep in mind that the default is trusting tutors, so instead whenever you are asked to enter y/n, you can just hit enter and 'yes' will be assumed")
    # print("You can try and edit the spreadsheet and restart if it's just a serious spelling error")
    # print("But the program can usually deal with most spelling errors")
    
    # This is where the Tracking logic goes

    for tutorRow in tutorRows:
        tutor = getTutor(tutorRow.name)
        if not tutor:
            print(f"Can't find tutor for {tutorRow.name}, skipping this row")
            continue

        tutorEntry = tutor.addTutorEntry(tutorRow)
        tuteeRow = findTuteeRow(tutor, tutorEntry)
        countHours = confirmHours(tutor, tutorRow, tuteeRow)
        print(f'{tutorRow.timestamp}= tutor: {tutorRow.name}; tutee: {tutorRow.tutee}')
        if tuteeRow:
            print(f'Found tutee row: {tuteeRow.timestamp}= tutor: {tuteeRow.tutor}; tutee: {tuteeRow.name}')
        else:
            if countHours:
                print("Found no tuteeRow, but counting hours") 
            else:
                print("found no tuteeRow, and not counting hours")
        
    
        # if not confirmed:
        #     (countHours, tuteeRow) = tryToConfirm(tuteeRow, tutorRow)
    
    
        if countHours:
            print("hours counted")
            tutor.addHours(tutorRow.length)
            if tuteeRow:
                tutor.addTuteeEntry(tuteeRow)

        # else:
        #     if tuteeRow:
        #         if confirmHours(tutor, tutorRow, tuteeRow):
        #             tutor.addTuteeEntry(tuteeRow)
        #             tutor.addHours(tutorRow.length)
        #         else:
        #             tutor.addTuteeEntry(tuteeRow)

        tutor.save()
