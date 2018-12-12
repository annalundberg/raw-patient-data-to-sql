#!/usr/bin/env python

import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Converts blanks into nulls")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    return parser.parse_args()


def main():
    # Get arguments from argparse
    args = get_arguments()
    # Use original filename & path to build output filename & path
    newfile = args.filename.split("/")
    newfile[-1] = 'tmp_' + newfile[-1]
    newfile = '/'.join(newfile)
    # Open original file to edit write changes in new file
    with open(args.filename, "r") as input, open(newfile, "w") as out:
        for line in input:
            line = line.split(",") # use list to split line into columns by ','
            for item in range(len(line)): # check each column
                if line[item] == "": # if column is empty, replace with NULL
                    line[item] = "NULL"
                elif line[item] == "\n": # if last column is empty, replace with 'NULL'+'\n'
                    line[item] = "NULL\n"
            # Line editing done, rejoin to csv and write to newfile
            line = ",".join(line)
            out.write(line)


if __name__ == "__main__":
    main()
