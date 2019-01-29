#!/usr/bin/env python

'''The goal here is to split a column containing ints and strings into
separate columns, one for ints and the other for strings.'''

import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Reformats results CSV by column")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    parser.add_argument("-c", "--columns", action='append',
                        help="columns to split, column per -c",
                        required=True, type=str)
    return parser.parse_args()


def is_float(bit):
    '''(string) -> bool
    This fxn checks a string to see if value is numeric, including floats AND
    exponential values ([0-9]+\.[0-9]+E.[0-9]+).
    >>>is_float('1.52')
    True
    >>>is_float('Th1s 15 a s3ntanc3.')
    False
    >>>is_float('38')
    True
    '''
    if re.match("^\d+\.\d+$", bit) is None: #if not a float
        if bit.isnumeric(): #is an integer
            return True
        elif re.match("^\d+\.\d+E.\d+$", bit) is None: #is not an exponential number
            if re.match("^\d+E.\d+$", bit) is None: #is not another format of exponential number
                return False
            else: #is an exponential number
                return True
        else: # is an exponential number
            return True
    else: #is a float
        return True


def sort_cols(ord_value):
    '''(string) -> tuple
    interprets column value, sort for int/string splitting and Returns
    a value for int column and comment column. In most cases the value
    will be sorted to one column and the other will read NULL.
    >>>sort_cols('3.55')
    '3.55', 'NULL'
    >>>sort_cols('Sample result')
    'NULL', 'Sample result'
    >>>sort_cols('>95')
    '96', 'above range'
    >>>sort_cols('<5')
    '4', 'below range'
    '''
    if is_float(ord_value): #any valid form of number (float, int, exponential)
        value = ord_value
        comment = 'NULL'
    elif ord_value == '': #blank column
        value = 'NULL'
        comment = 'NULL'
    elif ord_value.startswith('<'): #out of testing range, would be int
        value = ord_value[1:] #strip non-numeric character
        if is_float(value): #if valid number
            value = str(float(value)-1)
            comment = 'below range'
        else: #non-numeric
            value = 'NULL'
            comment = ord_value
    elif ord_value.startswith('>'): #out of testing range, would be int
        value = ord_value[1:]
        if is_float(value): #if valid number
            value = str(float(value)+1)
            comment = 'above range'
        else: #non-numberic
            value = 'NULL'
            comment = ord_value
    else: #non-numeric column
        value = 'NULL'
        comment = ord_value
    return value, comment


def conv_file(file, cols):
    '''(file, list) -> file
    This fxn reads in the file and uses list of columns to run fxn to split
    designated columns and re makes each line with the new column. Lines are
    then written into a newfile, designated with filename prefix tmp_'''
    # Use original filename & path to build output filename & path
    filename = file.split('/')
    filepath = "/".join(filename[:-1])
    new_file = filepath + "/tmp_" + filename[-1]
    # Open original file to edit write changes in new file
    with open(file) as f, open(new_file, 'w') as new_f:
        ln = 0
        for line in f:
            ln += 1
            added = 0
            entry = line.split(',') #split original csv file by column
            for col in range(len(cols)):
                n_col = int(cols[col])-1+added #adjust column for any added columns
                ord_value = entry[n_col]
                if ln == 1: #edit header column
                    value = 'NUMERIC_'+ord_value
                    comment = 'TEXT_'+ord_value
                else: #evaluate & edit values in column
                    value, comment = sort_cols(ord_value) #use fxn to sort column value
                entry = entry[0:n_col]+[value, comment]+entry[(n_col+1):len(entry)] #edit line with split values
                added += 1
            # Convert list back to csv line and write to newfile
            newline = ','.join(str(item) for item in entry)
            new_f.write(newline)
    return None


def main():
    '''runs internal fxns using argparse, see above fxns for details'''
    args = get_arguments()
    new = conv_file(args.filename, args.columns)
    return new


if __name__ == '__main__':
    main()
