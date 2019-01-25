#!/usr/bin/env python

import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Converts blanks into nulls")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    return parser.parse_args()


def main():
    args = get_arguments()
    filename = args.filename.split("/")
    filepath = "/".join(filename[:-1])
    with open(args.filename, "r") as input, \
            open(filepath + "/tmp_" + filename[-1], "w") as out:
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
