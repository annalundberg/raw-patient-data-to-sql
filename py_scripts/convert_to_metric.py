#!/usr/bin/env python

'''Convert height and/or weight to metric'''

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file, designates columns to convert to metric and current units")
    parser.add_argument("-f", "--filename", help="name of csv file",
                        required=True, type=str)
    parser.add_argument("-c", "--columns", action='append', help="columns to convert, column per -c",
                        required=True, type=int)
    parser.add_argument("-u", "--units", action='append', help="current units to be converted, 'oz' or 'inch'",
                        required=True, type=str)
    return parser.parse_args()

def inch_to_cm(height):
    '''(str)->float
    This fxn converts inches to cm'''
    if height != 'NA' and height != 'NULL': #avoid non-numic values
        height=float(height)*2.54 #conversion factor
    elif height == 'NA':
        height = 'NULL'
    return height

def oz_to_kg(weight):
    '''(str)->float
    This fxn converts ounces to kg'''
    if weight != 'NA' and weight != 'NULL': #avoid non-numeric values
        weight=float(weight)/35.274 #conversion factor
    elif weight == 'NA':
        weight = 'NULL'
    return weight

def convert(file, cols, unit):
    '''(file,list,str) -> None
    This fxn reads in .csv, and converts specified columns values to metric
    units. Ounces to kg and inches to cm.'''
    file_path = file.split('/')
    new_file = '../data/tmp_'+file_path[-1] # designate new file name & path
    ln = 0
    with open(file) as o_data, open(new_file, 'w') as n_file:
        for line in o_data:
            ln += 1
            entry = line.split(',') #split csv into list by columns
            if ln == 1:
                newline = line
            else:
                for i in range(len(cols)):
                    value = entry[cols[i]-1]
                    if unit[i] == 'oz':
                        entry[cols[i]-1] = oz_to_kg(value)
                    elif unit[i] == 'inch':
                        entry[cols[i]-1] = inch_to_cm(value)
                    else:
                        print('Error: invalid units')
                newline = ','.join(str(item) for item in entry)
            n_file.write(newline)
    return None

def main():
    '''runs metric conversions using argparse provided details'''
    args = get_arguments()
    convert(args.filename,args.columns,args.units)
    return None

if __name__ == '__main__':
    main()
