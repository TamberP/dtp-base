#!/usr/bin/env python3

import dtp_database
import sys

def print_help():
    print("DTP DB Lookup - Dumb Cli Version\n")
    print("Usage: " + sys.argv[0] + " [dtp number]\n")
    sys.exit(1)

def main():
    if(len(sys.argv) < 2):
        print_help()

    dtpsearch = sys.argv[1]
    dtp_database.db_connect()
    found = dtp_database.dtp_get(dtpsearch)
    print("Found " + str(len(found)) + " results.\n")

    for result in found:
        print("DTP: " +  result["DTP_Number"] + " - " + result["Make"] + " " + result["Type"])
        print("GVW: " + str(result["GVWDesign"]) + "kg", end='')
        if(result["GTWDesign"]):
            print("\t\tGTW: " + str(result["GTWDesign"]) + "kg\n")
        else:
            print("\n")

        if(len(found) > 1):
            print("Options:")
            for line in result["Suffixes"]:
                print(line)

        print("ABS: " + result["ABSFitted"])
        print("LSV: " + result["LSVFitted"])
        print("Park on diff: " + result["ParkOnDiff"])

        if(result["Axle3Weight"]):
            print("3rd Diff: " + result["ThirdDiff"])

        print("Service brake: " + result["ServiceType"] + " Secondary: " + result["SecondaryType"] + " Park: " + result["ParkType"])

        print("Axle 1: " + str(result["Axle1Weight"]) + "kg.\tModulated:" + result["Axle1Modulation"])
        print("Axle 2: " + str(result["Axle2Weight"]) + "kg.\tModulated:" + result["Axle2Modulation"])
        if(result["Axle3Weight"]):
            print("Axle 3: " + str(result["Axle3Weight"]) + "kg.\tModulated:" + result["Axle3Modulation"])
        if(result["Axle4Weight"]):
            print("Axle 4: " + str(result["Axle4Weight"]) + "kg.\tModulated:" + result["Axle4Modulation"])
        if(result["Axle5Weight"]):
            print("Axle 5: " + str(result["Axle5Weight"]) + "kg.\tModulated:" + result["Axle5Modulation"])

        print("Brake Routine")
        print(result["BrakeRoutine"])

if __name__ == "__main__":
    main()
