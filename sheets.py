import csv

import gspread
import config
import os
from datetime import datetime
from time import sleep
from utils import checkInName

client = gspread.oauth()

dataSH = client.open_by_url(config.DATA_SPREADSHEET_URL)
tutorSheets = dataSH.get_worksheet(1)
mainData = dataSH.get_worksheet(0)

tutorSH = client.open_by_url(config.TUTOR_SPREADSHEET_URL)
tuteeSH = client.open_by_url(config.TUTEE_SPREADSHEET_URL) 

tutorForm = tutorSH.get_worksheet(0).get_all_values()
tuteeForm = tuteeSH.get_worksheet(0).get_all_values()

tutorSHHeaders = tutorForm[0]
tuteeSHHeaders = tuteeForm[0]

specialDataFiles = [ "LAST_ROW" ]
lastRowFile = f'{config.LOCAL_DATA_FOLDER}/LAST_ROW'
open(lastRowFile, 'a').close()

tutorIndexes = {}
for value, header in config.TUTOR_HEADERS.items():
    tutorIndexes[value] = tutorSHHeaders.index(header)

tuteeIndexes = {}
for value, header in config.TUTEE_HEADERS.items():
    tuteeIndexes[value] = tuteeSHHeaders.index(header)

def getTutorSheet(name):
    ctsheets = getTutorSheet.ctsheets
    for ct in ctsheets:
        if checkInName(ct[0], name):
            return (True, client.open_by_url(ct[1]))
        
    sheet = client.create(name, folder_id=config.DATA_FOLDER_ID)
    # Make link viewable by anyone with link
    sheet.share(None, perm_type='anyone', role='reader', with_link=True)
    # Update info in sheet and reload ctsheets for future usage
    tutorSheets.update_cell(len(ctsheets)+1, 1, name)    
    tutorSheets.update_cell(len(ctsheets)+1, 2, sheet.url)    
    getTutorSheet.ctsheets = tutorSheets.get_all_values()

    return (False, sheet)
# this makes it so tutorsheets only calls sheets api when something changes
getTutorSheet.ctsheets = tutorSheets.get_all_values()

if not os.path.exists(config.LOCAL_DATA_FOLDER):
    os.makedirs(config.LOCAL_DATA_FOLDER)

def getLocalSheet(name):
    getSF = lambda n: f"{config.LOCAL_DATA_FOLDER}/{n}"
    for filename in os.listdir(config.LOCAL_DATA_FOLDER):
        if checkInName(filename, name):
            return getSF(filename)

    initCells = [['Hours:', '', 'Average Rating:', ''], \
    [], \
    ['Good Comments', '', 'Areas of Improvement']]
    rawsf = getSF(name)
    with open(rawsf, 'w') as sf:
        writer = csv.writer(sf)
        writer.writerows(initCells)

    return rawsf

"""
Google sheets api has a usage quota limit:
    100 requests per user per 100 seconds
    Read and write requests are tallied seperately
This is why the models cache data as csv files.
These functions are the only ones which actually 
the google sheets api.
So each function tallies it's own read/write requests
and returns each as a tuple.
_runDataFunc can run some function through a list 
and make sure the limit is not exceeded.
_loadData and _saveData are those functions which are run.
loadData and saveData are the exposed functions which run.py uses.
"""
def _runDataFunc(f, records):
    rcount = 0
    wcount = 0
    tnow = lambda: datetime.now()
    ptime = tnow()
    for record in records:
        tdelta = abs((tnow() - ptime).total_seconds())
        if tdelta >= 100:
            print("cool 100 seconds passed, time to reset it all")
            ptime = tnow()
            rcount = 0
            wcount = 0
        if rcount >= 45 or wcount >= 45:
            print("Ahhh exceeded, time to wait")
            # each function uses a maximum of 5 each, 
            # so it makes sense to stop at 95
            # if that ever changes these numbers should be changed.
            sleep(tdelta)
        (r, w) = f(record)
        print(f"reads: {r}, writes: {w}")
        rcount += r
        wcount += w    

def _loadData(line):
    rcount = 0
    with open(getLocalSheet(line[0]), 'w+') as clsh:
        lsh = csv.writer(clsh)       
        osh = client.open_by_url(line[1]).get_worksheet(0)
        rcount+=1
        lsh.writerows(osh.get_all_values())
        rcount+=1
    return (rcount, 0)

def loadData():
    records = tutorSheets.get_all_values()
    with open(lastRowFile, 'w') as cfile:
        crow = mainData.acell('B1').value
        if crow:
            cfile.write(str(crow))
        else:
            cfile.write('1')

    _runDataFunc(_loadData, records)

def _saveData(tfile):
    if tfile in specialDataFiles:
        return (0, 0)
    rcount = 0
    wcount = 0
    print(f'opening {tfile}')
    (exists, osh) = getTutorSheet(tfile)
    rcount += 1
    if not exists:
        print("said file does not exist")
        wcount += 3            
    with open(f'{config.LOCAL_DATA_FOLDER}/{tfile}', 'r') as lsh:
        print(f"importing the csv file that is {tfile}")
        data = list(csv.reader(lsh))
        osh.get_worksheet(0).update(data)
    wcount += 1
    return (rcount, wcount)

def saveData():
    records = os.listdir(config.LOCAL_DATA_FOLDER)
    with open(lastRowFile, 'r') as cfile:
        mainData.update_cell(1, 2, cfile.read())
    _runDataFunc(_saveData, records)
