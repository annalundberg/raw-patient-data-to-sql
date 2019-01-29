#!/usr/bin/env python

'''The purpose of this program is to collapse multiple equivalent data forms
into a single standardized form. (Ex. M and m will both be 'm')'''

import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file and designates columns to be edited")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    parser.add_argument("-c", "--columns", action='append', help="columns to split, 1 column per -c",
                        required=True, type=int)
    return parser.parse_args()

def is_float(bit):
    '''(string) -> bool
    This fxn checks a string to see if value is numeric, including floats AND
    exponential values ([0-9]+\.[0-9]+E.[0-9]+).
    >>>is_float('1.52')
    True
    >>>is_float('Th1s 15 a s3ntanc3.')
    False
    >>>is_float('52')
    True
    >>>is_float('5E-06')
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

def tumor_grade_collapse(grade):
    '''(string) -> string
    Collapsing equivalent tumor grade values for evaluation. General tumor
    grades were collapsed according to guidelines found in
    https://www.cancer.gov/about-cancer/diagnosis-staging/prognosis/tumor-grade-fact-sheet
    Other tumor grade collapsing handles simpler cases such as standardizing
    capitalization and number of spaces
    >>>tumor_grade_collapse('Generic Grade  Undifferentiated')
    'Generic Grade  Grade 4'
    >>>tumor_grade_collapse('Generic Grade  Grade 4')
    'Generic Grade  Grade 4'
    >>>tumor_grade_collapse('Gleason  Score 5(plus)4')
    'Gleason Score  5(plus)4'
    '''
    grade_dict = {'Generic Grade  Low Grade':'Generic Grade  Grade 1',
        'Generic Grade  Well differentiated':'Generic Grade  Grade 1',
        'Generic Grade  Grade 1':'Generic Grade  Grade 1',
        'Generic Grade  Grade 1-2':'Generic Grade  Grade 1-2',
        'Generic Grade  well to moderately differentiated':'Generic Grade  Grade 1-2',
        'Generic Grade  Well to moderately differentiated':'Generic Grade  Grade 1-2',
        'Generic Grade  Grade 2':'Generic Grade  Grade 2',
        'Generic Grade  Intermediate Grade':'Generic Grade  Grade 2',
        'Generic Grade  Moderately differentiated':'Generic Grade  Grade 2',
        'Generic Grade  Well to poorly differentiated':'Generic Grade  Grade 2',
        'Generic Grade  Grade 2-3':'Generic Grade  Grade 2-3',
        'Generic Grade  Moderate to poorly differentiated':'Generic Grade  Grade 2-3',
        'Generic Grade  Grade 3':'Generic Grade  Grade 3',
        'Generic Grade  Poorly differentiated':'Generic Grade  Grade 3',
        'Generic Grade  Poorly Differentiated':'Generic Grade  Grade 3',
        'Generic Grade  High Grade':'Generic Grade  Grade 3-4',
        'Generic Grade  Grade 4':'Generic Grade  Grade 4',
        'Generic Grade  Undifferentiated':'Generic Grade  Grade 4',
        'Generic Grade  Grade X':'Generic Grade  Grade X',
        'Generic Grade  Unfavorable Histology':'Generic Grade  Unfavorable Histology',
        'Generic Grade  Borderline':'Generic Grade  Borderline',
        'Generic Grade  Favorable Histology':'Generic Grade  Favorable Histology',
        'Bloom-Richardson  Grade 1':'Bloom-Richardson  Grade 1',
        'Bloom-Richardson  Grade 2':'Bloom-Richardson  Grade 2',
        'Bloom-Richardson  Grade 3':'Bloom-Richardson  Grade 3',
        'FIGO  Grade 1':'FIGO  Grade 1', 'FIGO  Grade 2':'FIGO  Grade 2',
        'FIGO  Grade 3':'FIGO  Grade 3', 'FNCLCC  Grade 1':'FNCLCC  Grade 1',
        'FNCLCC  Grade 2':'FNCLCC  Grade 2', 'FNCLCC  Grade 3':'FNCLCC  Grade 3',
        'FNCLCC  Grade 4':'FNCLCC  Grade 4', 'FNCLCC  Grade X':'FNCLCC  Grade X',
        'Fuhrman Nuclear  Grade 1':'Fuhrman Nuclear  Grade 1',
        'Fuhrman Nuclear  Grade 2':'Fuhrman Nuclear  Grade 2',
        'Fuhrman Nuclear  Grade 3':'Fuhrman Nuclear  Grade 3',
        'Fuhrman Nuclear  Grade 4':'Fuhrman Nuclear  Grade 4',
        'Gleason  Score 3(plus)2':'Gleason Score  3(plus)2',
        'Gleason  Score 3(plus)3':'Gleason Score  3(plus)3',
        'Gleason Score  3(plus)3':'Gleason Score  3(plus)3',
        'Gleason  Score 3(plus)4':'Gleason Score  3(plus)4',
        'Gleason Score  3(plus)4':'Gleason Score  3(plus)4',
        'Gleason Score  3(plus)5':'Gleason Score  3(plus)5',
        'Gleason  Score 4(plus)3':'Gleason Score  4(plus)3',
        'Gleason Score  4(plus)3':'Gleason Score  4(plus)3',
        'Gleason  Score 4(plus)4':'Gleason Score  4(plus)4',
        'Gleason Score  4(plus)4':'Gleason Score  4(plus)4',
        'Gleason  Score 4(plus)5':'Gleason Score  4(plus)5',
        'Gleason Score  4(plus)5':'Gleason Score  4(plus)5',
        'Gleason Score  5(plus)2':'Gleason Score  5(plus)2',
        'Gleason  Score 5(plus)3':'Gleason Score  5(plus)3',
        'Gleason score  5(plus)4':'Gleason Score  5(plus)4',
        'Gleason  Score 5(plus)4':'Gleason Score  5(plus)4',
        'Gleason Score  5(plus)4':'Gleason Score  5(plus)4',
        'Gleason  Score 5(plus)5':'Gleason Score  5(plus)5',
        'Gleason Score  5(plus)5':'Gleason Score  5(plus)5',
        'Modified Bloom-Richardson  Grade 1':'Modified Bloom-Richardson  Grade 1',
        'Modified Bloom-Richardson  Grade 2':'Modified Bloom-Richardson  Grade 2',
        'Modified Bloom-Richardson  Grade 3':'Modified Bloom-Richardson  Grade 3',
        'Not applicable':'NULL', 'Not documented in path report':'NULL',
        'Not Documented in Path Report':'NULL', 'NULL':'NULL',
        'WHO  Grade I':'WHO  Grade I', 'WHO  Grade II':'WHO  Grade II',
        'WHO  Grade III':'WHO  Grade III', 'WHO  Grade IV':'WHO  Grade IV',
        'WHO  Type AB':'WHO  Type AB'}
    if grade in grade_dict:
        grade = grade_dict[grade]
    else:
        print('Warning, unexpected grade encountered:', grade)
    return grade

def file_parse(file, cols):
    '''(file, list)->file
    parses a csv file and separates lines, collapses various known data variety
    in specified columns. Compatible when file is a csv'''
    filename = file.split('/')
    filepath = "/".join(filename[:-1])
    new_file = filepath + "/tmp_" + filename[-1]
    ln = 0
    with open(file) as o_data, open(new_file, 'w') as n_file:
        for line in o_data:
            ln += 1
            entry = line.split(',')
            if ln != 1:
                for i in range(len(cols)):
                    value = entry[int(cols[i])-1]
                    if cols[i]==6: # diagnosis column
                        if value == 'Unknown':
                            value = 'NULL'
                        elif value == 'Tumor of unknown origin':
                            value = 'Tumor of unknown origin or ill-defined site'
                    elif cols[i] == 7: # primary vs Metastasis
                        if value == 'metastatic' or value == 'Metastatic':
                            value = 'Metastasis'
                        elif value == 'primary' or value == 'Primary Tumor':
                            value = 'Primary'
                    elif cols[i] == 8 or cols[i] == 9 or cols[i] == 10 or cols[i] == 14 or cols[i] == 15 or cols[i] == 16: # T & N & M RDW
                        if value == 'NONE':
                            value = 'NULL'
                        elif value == 'Not applicable to 7th Edition staging':
                            value = 'NULL'
                    elif cols[i] == 12 or cols[i] == 13: # N & M Path User
                        if 'Not Documented in Path Report' in value:
                            value = 'NULL'
                    elif cols[i] == 22: # tumor grade
                        value = tumor_grade_collapse(value)
                    elif cols[i] == 25: # percent tumor
                        if value == 'below 5 percent' or value == 'below 5':
                            value = '4'
                        elif value == 'NULL':
                            value=value
                        elif int(value) > 100:
                            value = 'NULL'
                    elif cols[i] == 27: # percent necrosis
                        if value == 'above 95 percent':
                            value = '96'
                        elif value == 't':
                            value = 'NULL'
                        elif value == 'NULL':
                            value = 'NULL'
                        elif value == '96':
                            value = value
                        elif int(value) > 100:
                            value = 'NULL'
                    elif cols[i] == 28: # slide section area
                        if value == 'NULL':
                            value = 'NULL'
                            entry[int(cols[i])] = 'NULL'
                            swap = False
                        elif is_float(value):
                            value = value
                            swap = False
                        elif value == 'mm-2':
                            if entry[int(cols[i])] == 'NULL':
                                value = 'NULL'
                            else:
                                value = entry[int(cols[i])]
                                entry[int(cols[i])] = entry[int(cols[i])-1]
                        else:
                            swap = False
                    elif cols[i] == 29: # slide section area units
                        if value == 'NULL' or value == 'Area' or value == 'm' or value == 'Months':
                            value = 'NULL'
                        elif value == 'mm-2' or value == 'mm-2 ' or value == 'mm-2.':
                            value = 'mm-2'
                        elif value == 'cm-2' or value == 'um-2':
                            value = value
                        elif value == 'Micron':
                            value = 'um-2'
                    else: # columns not specified for processing
                        print('Unknown column, cannot simplify:', cols[i])
                    entry[int(cols[i])-1] = value
            newline = ','.join(str(item) for item in entry)
            n_file.write(newline)
    return None


def main():
    '''runs fxns for collapsing equivalent data. Uses arg parse to get file
    and columns to be converted.'''
    args = get_arguments()
    file_parse(args.filename, args.columns)
    return None


if __name__ == '__main__':
    main()
