#!/usr/bin/env python

# to convert time and data into sql smalldatetime format
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="reads in csv file, designates columns to convert time&date and designates type of separator")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    parser.add_argument("-c", "--columns", action='append', help="columns to split, column per -c",
                        required=True, type=str)
    parser.add_argument("-s", "--date_sep", help="date separator, choose slash or space",
                        required=True, type=str)
    return parser.parse_args()


def month_trans(month):
    '''(string)->string
    this fxn takes in a string containing month in 3 letter abbreviated form
    and converts it to its 2 digit numerical representation in a string.
    '''
    m_dict={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
            'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    return m_dict[month]


def timedate(date, time):
    '''(list)->str
    read list of month day year time to convert to sql compatible smalldatetime.
    Input format [mm,dd,yyyy]['hh','mm','ss','XM'].
    Output format is YYYY-MM-DD hh:mm:ss'''
    # Identify Year
    year = date[2]
    # Identify/check Month
    if len(date[0]) == 1:
        date[0] = '0'+date[0]
    month = date[0]
    # Identify/check Day
    if len(date[1]) == 1:
        date[1] = '0'+date[1]
    day = date[1]
    # Pull together date in proper format
    date = year+'-'+month+'-'+day
    # Check hour
    if len(time[0]) == 1:
        time[0] = '0'+time[0]
    # check for AM/PM & convert to military time
    if len(time) == 4:
        if 'AM' in time[3] and time[0] == '12':
            time[0] = '00'
        if 'PM' in time[3]:
            if time[0] != '12':
                time[0] = str(int(time[0])+12)
    # Rejoin time & date for output in final format
    time = ':'.join(str(bit) for bit in time[0:3])
    date_time = date+' '+time
    return date_time


def file_parse_sp(file, cols):
    '''(file)->file
    parses a csv file and separates lines, will incorporate other functions
    to convert time and date into sql smalldatetime format. Compatible when
    time/date is written as "Mon DD YYYY HH:MM:SS XM". AKA story format
    New timedate is YYYY-MM-DD hh:mm:ss'''
    # Use original filename & path to build output filename & path
    newfile = file.split("/")
    newfile[-1] = 'tmp_' + newfile[-1]
    newfile = '/'.join(newfile)
    ln = 0 # init line count
    # Open original file to edit write changes in new file
    with open(file) as o_data, open(newfile, 'w') as n_file:
        for line in o_data:
            ln += 1
            entry = line.split(',') #split csv into list by columns
            if ln == 1: #header
                newline = entry #no edit needed
            else:
                # Timedate conversion for each specified column
                for i in range(len(cols)):
                    date_time = entry[int(cols[i])-1]  # 'Mon DD YYYY 12:00:00 AM'
                    date_time = date_time.split(' ') # split date & time into list
                    date_time[0] = month_trans(date_time[0]) # Mon -> MM
                    date = date_time[0:3] # isolate date list
                    time = date_time[3].split(':')  # result: ['hh','mm','ss']
                    if len(date_time) == 5: # If time includes AM/PM
                        time.append(date_time[4]) # Include AM/PM to time list
                    entry[int(cols[i])-1] = timedate(date, time) # Update entry
            # Convert list back to csv line and write to newfile
            newline = ','.join(str(item) for item in entry)
            n_file.write(newline)
    return None


def file_parse_sl(file, cols):
    '''(file)->file
    parses a csv file and separates lines, will incorporate other functions
    to convert time and date into sql smalldatetime format. Compatible when
    date is in MM/DD/YYYY HH:MM:SS format in a csv'''
    # Use original filename & path to build output filename & path
    newfile = file.split("/")
    newfile[-1] = 'tmp_' + newfile[-1]
    newfile = '/'.join(newfile)
    ln = 0 # init line count
    # Open original file to edit write changes in new file
    with open(file) as o_data, open(newfile, 'w') as n_file:
        for line in o_data:
            ln += 1
            entry = line.split(',') #split csv into list by columns
            # header needs no edit
            if ln == 1:
                newline = entry
            else:
                # Timedate conversion for each specified column
                for i in range(len(cols)):
                    date_time = entry[int(cols[i])-1]
                    if len(date_time) == 0 or date_time[0] == 'NULL': # handle blank column
                        break
                    date_time = date_time.split(' ') # Split date and time
                    date = date_time[0]
                    if len(date_time) == 1 or date_time[1] == 'NULL': # no time entry
                        time = '00:00:00'.split(':') # default time added
                    else:
                        time = date_time[1].split(':')
                    if len(time) == 2: # add seconds if needed
                        time.append('00')
                    if len(date_time) == 3: # add AM/PM if present
                        time.append(date_time[2])
                    date = date.split('/')  # resulting format ['MM','DD','YYYY']
                    entry[int(cols[i])-1] = timedate(date, time)
            # Convert list back to csv line and write to newfile
            newline = ','.join(str(item) for item in entry)
            n_file.write(newline)
    return None


def main():
    '''runs fxns for converting date and time into smalldatetime format. uses
    arg parse to get file, columns to be converted and the type of date present.'''
    args = get_arguments()
    # handle MM/DD/YYYY format
    if args.date_sep == 'slash':
        file_parse_sl(args.filename, args.columns)
    # handle Mon DD YYYY format
    elif args.date_sep == 'space':
        file_parse_sp(args.filename, args.columns)
    # currently other formats not supported
    else:
        print('Invalid date separator given. Choose "slash" or "space".')
    return None


if __name__ == '__main__':
    main()
