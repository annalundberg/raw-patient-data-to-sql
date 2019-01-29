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

echo "ADDING PATIENT IDS MISSING FROM DEMOGRAPHICS"
## Add patient IDs to missing from demographics table present in other tables ##
cat $csv_file > $tmp_file
# Use missing ID list to add entries in demographics table
while read id; do
  line=$id,NULL,Unknown,Unknown,U,U,NULL;
  echo $line >> $tmp_file
done < $data_path/data/subjectID_to_add.txt
mv $tmp_file $csv_file
## Add patient IDs from staging
./add_unknown_subjectids_new.sh
