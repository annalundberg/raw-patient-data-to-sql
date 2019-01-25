#!/usr/bin/env python

'''Fix scientific notation E's fit SQL float format.'''

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(
        description="Changes scientific notation to float in numeric_order_value column from results")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    parser.add_argument("-o", "--output", help="output file name",
                        required=True, type=str)
    return parser.parse_args()

def main():
    args = get_arguments()
    file = args.filename
    out = args.output
    with open(file, "r") as fh:
        with open(out, "w") as ofh:
            lc = 0
            for line in fh:
                lc += 1
                if lc == 1:
                    ofh.write(line)
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
                        ofh.write(",".join(line))
                    else:
                        ofh.write(",".join(line))
    return None

if __name__ == '__main__':
    main()
