#!/usr/bin/env python

'''The goal here is to fill all blank columns with SQL friendly NULL. NA and
other forms of NA will also be converted to NULL for SQL'''

import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Converts blanks into nulls")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    return parser.parse_args()


def main():
    '''() -> file
    Uses argparse to get input file. Creates new file for changes to be written
    into, designated with tmp_ prefix. Blank columns are filled with NULL,
    NA and Not applicable column values are replaced with NULL'''
    args = get_arguments()
    file = args.filename
    filename = file.split('/')
    filepath = "/".join(filename[:-1])
    new_file = filepath + "/tmp_" + filename[-1]
    with open(file, "r") as input, open(new_file, "w") as out:
        for line in input:
            line = line.split(",")
            for item in range(len(line)):
                if line[item] == "":
                    line[item] = "NULL"
                elif line[item] == "\n":
                    line[item] = "NULL\n"
                elif line[item] == "NA":
                    line[item] = "NULL"
                elif line[item] == "Not applicable":
                    line[item] = "NULL"
            line = ",".join(line)
            out.write(line)


if __name__ == "__main__":
    main()
