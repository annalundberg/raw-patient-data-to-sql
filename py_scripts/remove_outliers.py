#!/usr/bin/env python

'''Remove outliers in visits. Outliers have been previously identified for
removal, they are unreasonably high values of height and BMI. The following
code is aimed at fixing this specific case'''

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file for removing outliers")
    parser.add_argument("-f", "--filename", help="name of csv file",
                        required=True, type=str)
    return parser.parse_args()

def remove_out(file):
    '''(file) -> file
    This fxn reads in .csv, and removes unreasonably high values FROM
    height and BMI. Writes changes into new file designated by prefix
    temp_ '''
    filename = file.split('/')
    filepath = "/".join(filename[:-1])
    new_file = filepath + "/tmp_" + filename[-1]
    ln = 0
    with open(file) as o_data, open(new_file, 'w') as n_file:
        for line in o_data:
            ln += 1
            entry = line.split(',')
            if ln == 1:
                newline = line
            else:
                if entry[4] != 'NA':
                    if float(entry[4]) > 100:
                        entry[4] = 'NA'
                if entry[3] != 'NA':
                    if float(entry[3]) > 90:
                        entry[3] = 'NA'
                newline = ','.join(str(item) for item in entry)
            n_file.write(newline)
    return None

def main():
    '''runs specified outlier removal using argparse provided details'''
    args = get_arguments()
    remove_out(args.filename)
    return None

if __name__ == '__main__':
    main()
