#!/usr/bin/env bash

echo "SET FILES"

data_path="<path_to_datafiles>"
infile=$data_path"/data/Demographics.csv"
csv_file=$data_path'/data/cleaned_demographics.csv'
tmp_file=$data_path'/data/tmp_cleaned_demographics.csv'

## Clean up problematic characters
## grep -Eo '[^A-Za-z0-9.(), -]' $csv_file | sort | uniq -c | sort
# characters found: _ ? /

echo "FIXING PROBLEMATIC CHARACTERS"

cat $infile | tr '_' '.' | tr '?' '-' | tr '/' '-' \
> $csv_file


echo "CONVERTING BLANKS TO NULLS"

../py_scripts/blanks_to_nulls.py -f $csv_file
mv $tmp_file $csv_file
