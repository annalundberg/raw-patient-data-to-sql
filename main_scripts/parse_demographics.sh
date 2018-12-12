#!/usr/bin/env bash

## Pipeline for Demographics csv cleaning ##

echo "SET FILES"
## Edit this section to direct pipeline to your files ##
data_path="<path_to_datafiles>"
infile=$data_path"/data/Demographics.csv"
csv_file=$data_path'/data/cleaned_demographics.csv'
tmp_file=$data_path'/data/tmp_cleaned_demographics.csv'

## Find problematic characters (for SQL) to clean up ##
## grep -Eo '[^A-Za-z0-9.(), -]' $csv_file | sort | uniq -c | sort
# characters found: _ ? /

echo "FIXING PROBLEMATIC CHARACTERS"
## Cleaning problematic characters found above ##
cat $infile | tr '_' '.' | tr '?' '-' | tr '/' '-' \
> $csv_file


echo "CONVERTING BLANKS TO NULLS"
## Converts blank columns to 'NULL' ##
../py_scripts/blanks_to_nulls.py -f $csv_file
mv $tmp_file $csv_file
