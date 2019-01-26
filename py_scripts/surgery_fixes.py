#!/usr/bin/env python

'''Fix words that contain NA that accidentally were changed to NULL.'''

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

with open(file, "r") as fh:
    with open(new_file, "w") as oFH:
        for line in fh:
            line = line.split(",")

            # Edit PIP9X: PRIMARY.ICD9.PX.NAME
            if "NULL " in line[6]:
                line[6] = line[6].replace("NULL ", "NA")

            # Edit SPD: SURGERY.PROC.DESC
            if "NULL " in line[9]:
                line[9] = line[9].replace("NULL ", "NA")

            # Edit AT: ANESTHESIA.TYPE
            if "NULL " in line[10]:
                line[10] = line[10].replace("NULL ", "NA")

            oFH.write(",".join(line))
