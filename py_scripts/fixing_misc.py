#!/usr/bin/env python

'''Fix E's in numeric_order_value from misc table (used by parse_results) 
to fit SQL float format.'''

import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file for E fixing")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    return parser.parse_args()

def fix(file):
    '''(file) -> file
    Returns numberic 'e' notation to floats from misc table,
    for SQL compatibility'''
    filename = file.split('/')
    filepath = "/".join(filename[:-1])
    new_file = filepath + "/tmp_" + filename[-1]
    with open(file, "r") as fh, open(new_file, "w") as oFH:
        lc = 0
        for line in fh:
            lc += 1
            if lc == 1:
                oFH.write(line)
            else:
                if ",NA," in line:
                    line = line.replace(",NA,", ",NULL,")
                line = line.split(",")
                NOV = line[10]
                if "E" in NOV:
                    if NOV == "20E89500":
                        NOV = "NULL"
                    else:
                        NOV = float(NOV.split("E")[0]) * (10 ** float(NOV.split("E")[1]))
                    line[10] = str(NOV)
                    oFH.write(",".join(line))
                else:
                    oFH.write(",".join(line))
    return None

def main():
    '''runs fxn for fixing float value notation using argparse
    to get file'''
    args = get_arguments()
    fix(args.filename)
    return None

if __name__ == '__main__':
    main()
