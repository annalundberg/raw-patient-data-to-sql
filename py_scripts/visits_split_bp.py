#!/usr/bin/env python

'''Split BP into SYSTOLIC and DIASTOLIC pressure in visits table.'''


import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file, designates columns to convert time&date and designates type of separator")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    return parser.parse_args()

args = get_arguments()
file = args.filename
filename = file.split('/')
filepath = "/".join(filename[:-1])
new_file = filepath + "/tmp_" + filename[-1]

lc = 0
SYSTOLE = ""
DIASTOLE = ""
with open(file, "r") as fh:
    with open(new_file, "w") as oFH:
        for line in fh:
            lc += 1
            if lc == 1:
                string1 = "SUBJECT.ID,VISIT.DATE.TIME,WEIGHT,MOST.CURRENT.HEIGHT,BMI,BP.SYSTOLE,BP.DIASTOLE,"
                string2 = "ENCOUNTER.DIAGNOSIS.ICD9,ENCOUNTER.DIAGNOSIS.ICD10\n"
                string = string1 + string2
                oFH.write(string)
            elif lc > 1:
                SI = line.strip("/n").split(",")[0]
                VD = line.strip("/n").split(",")[1]
                W = line.strip("/n").split(",")[2]
                H = line.strip("/n").split(",")[3]
                BMI = line.strip("/n").split(",")[4]
                BP = line.strip("/n").split(",")[5]
                I9 = line.strip("/n").split(",")[6]
                I10 = line.strip("/n").split(",")[7]

                if BP == "NULL":
                    SYSTOLE = "NULL"
                    DIASTOLE = "NULL"
                else:
                    BP = BP.split("-")
                    SYSTOLE = BP[0]
                    DIASTOLE = BP[1]

                string1 = SI + "," + VD + "," + W + "," + H + "," + BMI + "," + SYSTOLE + ","
                string2 = DIASTOLE + "," + I9 + "," + I10
                string = string1 + string2
                oFH.write(string)
