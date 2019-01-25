#!/usr/bin/env python

'''Remove unreasonable ages in staging. Ages that are unreasonable are removed,
such as negative ages. The following code is aimed at fixing this
specific case'''

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file for removing outliers")
    parser.add_argument("-f", "--filename", help="name of csv file",
                        required=True, type=str)
    return parser.parse_args()

def convert(file):
    '''This fxn reads in .csv, and removes unreasonable values FROM
    age'''
    filename = file.split('/')
    filepath = "/".join(filename[:-1])
    new_file = filepath + "/tmp_" + filename[-1]
    ln = 0
    with open(file) as o_data, open(new_file, 'w') as n_file:
        for line in o_data:
            ln += 1
            entry = line.split(',')
            if ln != 1:
                if float(entry[1]) < 0:
                    entry[1] = 'NULL'
            newline = ','.join(str(item) for item in entry)
            n_file.write(newline)
    return None

def main():
    '''runs unreasonable age removal'''
    args = get_arguments()
    convert(args.filename)
    return None

if __name__ == '__main__':
    main()
