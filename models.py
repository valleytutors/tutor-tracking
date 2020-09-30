import csv
import sheets
import random
import requests
import time
from remote import getTutor

class TutorRow:
    indexes = {}
    def __init__(self, row, rowNumber):
        c = TutorRow.indexes
        getKey = lambda k: row[c[k]] if k in c else None
        self.rawRow = row
        self.name = getKey('name')
        self.tutee = getKey('tutee')
        self.length = int(getKey('length'))
        self.rating = int(getKey('rating'))
        self.completion = getKey('completion') == "Meeting Was Completed"
        self.timestamp = getKey('timestamp')
        self.date = getKey('date')
        self.rowNumber = rowNumber
    
    def __str__(self):
        return str(self.rawRow)

class TuteeRow:
    indexes = {}
    def __init__(self, row, rowNumber):
        c = TuteeRow.indexes
        getKey = lambda k: row[c[k]] if k in c else None
        self.rawRow = row
        self.name = getKey('name')
        self.tutor = getKey('tutor')
        self.length = getKey('length')
        self.rating = int(getKey('rating'))
        self.completion = getKey('completion') == "The meeting was complete"
        self.timestamp = getKey('timestamp')
        self.date = getKey('date')
        self.wentWell = getKey('wentWell')
        self.improvements = getKey('improvements')
        self.rowNumber = rowNumber

    def __str__(self):
        return str(self.rawRow)


class Tutor:
    def __init__(self, name):
        self.name = name
        # Hours refers to the time volunteered and is in hours
        self.page = getTutor(self.name)
        if not self.page:
            raise NameError(f"can't find page for {name}")
            

        self.hours = self.page.hours
        if self.hours == None:
            self.hours = 0
        else:
            self.hours = int(self.hours)
        # Number of entries in tutor spreadsheet
        self.countText = self.page.sessions
        if self.countText:
            ct = self.countText.split('(')
            # text is formated count(rcount)
            self.count = int(ct[0])
            self.rcount = int(ct[1][0])
        else:
            self.count = 0
            self.rcount = 0

        self.rating = self.page.average_rating
        if self.rating == None:
            self.rating = 0.0
        else:
            self.rating = float(self.rating)


        # List of tuples
        # (count, rowEntry)
        self.tutorEntries = []
        self.tuteeEntries = []


        # self.sheetFile = sheets.getLocalSheet(self.name)
        # self.sheet = csv.writer(open(self.sheetFile, 'a'))    

        """
        with open(self.sheetFile, 'r') as cfile: 
            cstate = list(csv.reader(cfile))
            if cstate[0][1]:
                self.hours = float(cstate[0][1])
            if len(cstate) > 3:
                c = len(cstate) - 3
                self.count = c
                self.prevCount = c
                self.prevRating = float(cstate[0][3])

        """

    # def load(self):
    #                             

    # def save(self):
    #     wentWells = []
    #     improvements = []
    #     for entry in self.tuteeEntries:
    #         wentWells.append(entry.wentWell)
    #         wentPoorly.append(entry.improvements)
    #     random.shuffle(improvements)


    def addTutorEntry(self, row: TutorRow):
        centry = (self.count, row)
        self.tutorEntries.append(centry)
        if row.date:
            self.page.Dates = self.page.Dates + f'{row.date}({row.length})\n,'
        else:
            date = row.timestamp.split()[0]
            self.page.Dates = self.page.Dates + f'{date}({row.length})\n,'

        self.count += 1
        return centry

    def addTuteeEntry(self, row: TuteeRow):
        self.tuteeEntries.append(row)
        self.addRating(row.rating)
        # self.sheet.writerow([row.wentWell, '', row.improvements])
        return row

    def addHours(self, hours, inMinutes=True):
        # The spreadsheet is in minutes so thats the default 
        if inMinutes:
            self.hours += hours/60
        else:
            self.hours += hours
        # self.saveHours()

    def addRating(self, newRating):
        # Will update count too, since thats mainly for rating calc
        self.rcount += 1
        self.rating = (self.rating*(self.rcount-1)\
                        +newRating)/self.rcount
    
    def _save(self):
        self.page.hours = self.hours
        self.page.average_rating = self.rating
        self.page.sessions = f'{self.count}({self.rcount})'

    def save(self):
        while True:
            try:
                self._save()
            except requests.exceptions.HTTPError:
                time.sleep(1)
            else:
                break




    """
    def saveHours(self):
        rsheet = open(self.sheetFile, 'r')
        cstate = list(csv.reader(rsheet))
        cstate[0][1] = self.hours
        cstate[0][3] = self.avgRating()
        wsheet = open(self.sheetFile, 'w')
        writer = csv.writer(wsheet)
        writer.writerows(cstate)
        rsheet.close()
        wsheet.close()

    def avgRating(self):
        ratings = [entry.rating for entry in self.tuteeEntries]
        avg = (sum(ratings)+self.prevRating*self.prevCount)/self.count
        return avg
    """



