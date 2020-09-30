from sys import argv
cmd = argv[1]

if cmd == "load":
    print("##LOADING DATA FROM GOOGLE SPREADSHEETS##")
    from sheets import loadData
    loadData()

if cmd == "track":
    print("##TRACKING TUTORS##")
    import track
    track.trackTutors()

"""
if cmd == "save":
    print("##BEFORE STARTING THIS##")
    print("Please backup the current data folder by making a copy in google drive")
    print("##SAVING DATA(DO NOT QUIT DURING THIS")
    print("--If this does quit in the middle please ask for help--")
    print("--Fixing any data problems requires an intimate knowledge of the code--")
    print("Although if you saved a backup, just copy that, rename and run again")
    from sheets import saveData
    saveData()
"""
