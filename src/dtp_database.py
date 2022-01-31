# Functions for interacting with the DTp database
import sqlite3
import csv

global db_conn
global db_curs

def db_connect():
    global db_conn
    global db_curs
    db_conn = sqlite3.connect('../DTP-base.sqlite')
    db_conn.row_factory = sqlite3.Row
    db_curs = db_conn.cursor()

def db_version():
    return db_curs.execute("SELECT * FROM Version;").fetchone()

# Fetch the raw DTP data from the database
def dtp_fetch(dtp_num):
    return db_curs.execute("SELECT * FROM Master WHERE DtpNumber=(?);", (dtp_num,)).fetchall()

# Given a vehicle make ID, return the human-readable manufacturer's name/make
def vehMake(makeid):
    row = db_curs.execute("SELECT Make FROM VehMake WHERE MakeId=(?);", (makeid,)).fetchone()
    return row["Make"]

# Populate given lists with the Vehicle Make IDs and human readable names
def get_vehMakes(makes, ids):
    tmp = db_curs.execute("SELECT * FROM VehMake ORDER BY Make;").fetchall()
    if(tmp is not None):
        for row in tmp:
            makes.append(row[1])
            ids.append(row[0])
    return

# Given a vehicle type ID, return the human-readable vehicle type
def vehType(typeid):
    row = db_curs.execute("SELECT Type FROM VehType WHERE TypeId=(?);", (typeid,)).fetchone()
    return row["Type"]

# Given a trailer DTp number, fetch the raw trailer-weight info
def dtp_trl_fetch(dtp_num):
    return db_curs.execute("SELECT * FROM TrailerWeights WHERE DTpNumber=(?);", (dtp_num,)).fetchone()

# TODO: This needs to be able to return enough info that we can use it to figure out what questions to ask
# and then -- from those answers -- pull in the correct data.
def dtp_suffixes(dtp_suf):
    suffixes = []
    for suf in list(dtp_suf):
        # Oh god. Revisit this when you get python 3.10, where they actually
        # added match/case.
        if suf == 'G':
            suffixes.append("Drum brakes or disk brakes?")
        elif suf == 'H':
            suffixes.append("Two or three position hand-control fitted?")
        elif suf == 'I':
            suffixes.append("Park brake on Axles 1&4, 2&4, or 2&3?")
        elif suf == 'J':
            suffixes.append("Type 24 or Twinstop 12/30 actuator on front axle?")
        elif suf == 'K':
            suffixes.append("Park brake on axle 1?")
        elif suf == 'L':
            suffixes.append("Secondary & park brake on axle 1?")
        elif suf == 'M':
            suffixes.append("Park brake on axle 2?")
        elif suf == 'N':
            suffixes.append("Secondary & park brake on axle 2?")
        elif suf == 'O':
            suffixes.append("Park brake on Axles 1&2, 1&3, or 2 only?")
        elif suf == 'P':
            suffixes.append("Secondary & park brake on Axle 4?")
        elif suf == 'S':
            suffixes.append("Second alternative")
        elif suf == 'T':
            suffixes.append("Third option when I is used")
        elif suf == 'U':
            suffixes.append("Third option when O is used")
        else:
            suffixes.append("Unknown code.")
    return suffixes

# Translate a brake type id into its human readable description.
# e.g. HYDRAULIC, or AIR
def dtp_braketype(typenum):
    if(typenum is not None):
        row = db_curs.execute("SELECT Type FROM BrakType WHERE TypeId=(?)", (typenum,)).fetchone()
        return row["Type"]
    else:
        return "NONE"

# Translate a brake routine number, to a human readable string that
# tells you what axles should be tested for what.
# e.g. 1+2, SPLIT, 2 is "service brake on both axles, split service brake, park on axle 2"
def dtp_brakeroutine(routinenum):
    row = db_curs.execute("SELECT `Routine` FROM BrakRoute WHERE RoutineId=(?)", (routinenum,)).fetchone()
    routine = []
    if(row is not None):
        for stringle in row["Routine"].split(","):
            routine.append(stringle.strip())
    else:
        routine = ["","",""]
    return routine

def dtp_splitroutine(routinenum):
    routine = db_curs.execute("SELECT `Routine` from SplitRoutine WHERE RoutineId=(?)", (routinenum,)).fetchone()
    if(routine is not None):
        return routine["Routine"]
    else:
        return "NONE"

# Given a DTp number, return a vaguely human-readable-ish form of the
# stuff in the DB.  Multiple records can be returned for the same DTp,
# depending on options!

# (e.g. option for park on axle 1 results in 2 records, one for with
# first axle park, one for without.
def dtp_get(dtp_num):
    deeteepees = []
    for row in dtp_fetch(dtp_num):
        deeteepees.append(dtp_rowparse(row))
    return deeteepees

def dtp_get_make(searchmake):
    deeteepees = []
    tmp = db_curs.execute("SELECT MakeId FROM VehMake WHERE Make=(?);", (searchmake.upper(),)).fetchone()
    make_id = tmp["MakeId"]

    if(make_id is not None):
        tmp = db_curs.execute("SELECT * FROM Master WHERE MakeId=(?);", (make_id,)).fetchall()
        if(tmp is not None):
            for row in tmp:
                deeteepees.append(dtp_rowparse(row))
    return deeteepees


# Chew up a raw database row and reference the other tables.
def dtp_rowparse(raw):
    if(raw is not None):
        testdata = {}
        testdata["DTP_Number"] = raw["DTpNumber"]
        testdata["Make"] = vehMake(raw["MakeId"])
        testdata["Type"] = vehType(raw["TypeId"])
        testdata["Suffixes"] = dtp_suffixes(raw["DuplicateID"]) if (raw["DuplicateID"] is not None) else ''
        testdata["Second_Front_Axle_Steer"] = 'Yes' if(raw["SecFrontAxleSteered"] == 1) else 'No'
        testdata["Trans_Sec_Park_Brake"] = 'Yes' if(raw["TransSecParkBrake"] == 1) else 'No'
        testdata["Secondary_only_Tractor"] = 'Yes' if(raw["SecBrakeOnlyOnTrac"] == 1) else 'No'
        testdata["PrePriorPost68"] = 'Yes' if(raw["PPPSelector"] == 1) else 'No'
        testdata["GVWDesign"] = (raw["GVW_DesignWeight"] * 10)
        testdata["GTWDesign"] = (raw["GTW_DesignWeight"] * 10)
        testdata["Axle1Weight"] = (raw["Axle1DesignWeight"] * 10)
        testdata["Axle2Weight"] = (raw["Axle2DesignWeight"] * 10)
        testdata["Axle3Weight"] = (raw["Axle3DesignWeight"] * 10)
        testdata["Axle4Weight"] = (raw["Axle4DesignWeight"] * 10)
        testdata["Axle5Weight"] = (raw["Axle5DesignWeight"] * 10)
        testdata["Axle1Modulation"] = 'Yes' if(raw["ModAxle1Affect"] == 1) else 'No'
        testdata["Axle2Modulation"] = 'Yes' if(raw["ModAxle2Affect"] == 1) else 'No'
        testdata["Axle3Modulation"] = 'Yes' if(raw["ModAxle3Affect"] == 1) else 'No'
        testdata["Axle4Modulation"] = 'Yes' if(raw["ModAxle4Affect"] == 1) else 'No'
        testdata["Axle5Modulation"] = 'Yes' if(raw["ModAxle5Affect"] == 1) else 'No'
        testdata["ABSFitted"] = 'Yes' if(raw["ABSFitted"] == 1) else 'No'
        testdata["ABSOption"] = 'Yes' if(raw["ABSOption"] == 1) else 'No'
        testdata["LSVFitted"] = 'Yes' if(raw["LSVFitted"] == 1) else 'No'
        testdata["LSVOption"] = 'Yes' if(raw["LSVOption"] == 1) else 'No'
        testdata["DoubleDrive"] = 'Yes' if(raw["DoubleDriveFitted"] == 1) else 'No'
        testdata["ThirdDiff"] = 'Yes' if(raw["AskThirdDiffFitted"] == 1) else 'No'
        testdata["ParkOnDiff"] = 'Yes' if(raw["SecParkBrakeOnDiffAxle"] == 1) else 'No'
        testdata["ServBrakeDist"] = raw["ServiceBrakeDestrib"]
        testdata["SecBrakeDist"] = (raw["SecBrakeDestrib"]) if(raw["SecBrakeDestrib"] != 99) else 100
        testdata["ServiceType"] = dtp_braketype(raw["FoundServBrake"])
        testdata["SecondaryType"] = dtp_braketype(raw["FoundSecBrake"])
        testdata["ParkType"] = dtp_braketype(raw["FoundParkBrake"])
        testdata["BrakeRoutine"] = dtp_brakeroutine(raw["BrakeRoutine"])
        testdata["SplitRoutine"] = dtp_splitroutine(raw["SplitRoutine"])

        return testdata
    else:
        return None
