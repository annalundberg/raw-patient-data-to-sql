#!/usr/bin/env python

'''Remove outliers in visits. Outliers identified for removal are unreasonably
high values of height and BMI. The following code is aimed at fixing This
specific case'''

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file for removing outliers")
    parser.add_argument("-f", "--filename", help="name of csv file",
                        required=True, type=str)
    return parser.parse_args()

def convert(file):
    '''This fxn reads in .csv, and removes unreasonably high values FROM
    height and BMI'''
    # Use original filename & path to build output filename & path
    newfile = file.split("/")
    newfile[-1] = 'tmp_' + newfile[-1]
    newfile = '/'.join(newfile)
    ln = 0 # init line counter
    # Open original file to edit write changes in new file
    with open(file) as o_data, open(newfile, 'w') as n_file:
        for line in o_data:
            ln += 1
            entry = line.split(',') #split csv into list by columns
            if ln == 1: # header
                newline = entry # no edits necessary
            else:
                if entry[4] != 'NA': # avoid blank columns
                    if float(entry[4]) > 100: # target known outlier
                        entry[4] = 'NA'  # convert outlier to NA
                if entry[3] != 'NA': # avoid blank columns
                    if float(entry[3]) > 90: #target known outlier
                        entry[3] = 'NA' # avoid blank columns
            # Convert list back to csv line and write to newfile
            newline = ','.join(str(item) for item in entry)
            n_file.write(newline)
    return None

def main():
    '''runs metric conversions using argparse provided details'''
    args = get_arguments()
    convert(args.filename)
    return None

if __name__ == '__main__':
    main()
