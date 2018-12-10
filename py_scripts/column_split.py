#!/usr/bin/env python

'''The goal here is to split a column containing ints and strings into
separate columns, 1 for ints and the other for strings.'''

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


def sort_cols(ord_value, ncol):
    '''(string,int)->list
    interprets column value, sort for int/string splitting and Returns
    a value for int column and comment column'''
    if is_float(ord_value): #any valid form of number (float, int, exponential)
        value = ord_value
        comment = 'NULL'
    elif ord_value == '': #blank column
        value = 'NULL'
        comment = 'NULL'
    elif ord_value.startswith('<'): #out of testing range, would be int
        value = ord_value[1:] #strip non-numeric character
        if is_float(value): #if valid number
            value = float(value)-1
            comment = 'below range'
        else: #non-numeric
            value = 'NULL'
            comment = ord_value
    elif ord_value.startswith('>'): #out of testing range, would be int
        value = ord_value[1:]
        if is_float(value): #if valid number
            value = float(value)+1
            comment = 'above range'
        else: #non-numberic
            value = 'NULL'
            comment = ord_value
    else: #non-numeric column
        value = 'NULL'
        comment = ord_value
    return value, comment


def conv_file(file, cols):
    '''(file, list)->File
    This fxn reads in the file and handles fxn to split column and re makes
    each line with the new column'''
    file_path = file.split('/') #split up file path & file name
    new_file = '../data/tmp_'+file_path[-1] #make path & new name of new file
    with open(file) as f, open(new_file, 'w') as new_f: #open original file in read & new file to write
        ln = 0
        for line in f: #iterate through lines of original file
            ln += 1
            entry = line.split(',') #split original csv file by column
            added = 0 #init count for added columns
            for col in range(len(cols)): #perform the following for each column in list(cols)
                n_col = int(cols[col])-1+added #adjust column for any added columns
                ord_value = entry[n_col] 
                if ln == 1: #edit header column
                    value = 'NUMERIC_'+ord_value
                    comment = 'TEXT_'+ord_value
                else: #evaluate & edit values in column
                    value, comment = sort_cols(ord_value, n_col) #use fxn to sort column value
                entry = entry[0:n_col]+[value, comment]+entry[(n_col+1):len(entry)] #add split columns to line
                added += 1
            newline = ','.join(str(item) for item in entry) #convert line back to csv string
            new_f.write(newline) #add line to new file
    return new_file


def main():
    '''runs internal fxn'''
    args = get_arguments()
    new = conv_file(args.filename, args.columns)
    return new


if __name__ == '__main__':
    main()
