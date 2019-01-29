#!/usr/bin/env bash

echo "CONVERTING FROM CSV TO TSV FOR PROCESSING"

#Convert the original file to a tsv, also remove the one row without a patient ID
Rscript ../r_scripts/surgery_to_tsv.R

# File
data_path="<path_to_datafiles>"
infile=$data_path"/data/surgery.tsv"
csv_file=$data_path"/data/cleaned_surgery.csv"
tmp_file=$data_path"/data/tmp_cleaned_surgery.csv"

echo "REFORMATTING CHARACTERS, CONVERTING BACK TO CSV"

# remove ',' and '"' to allow processing as a csv later
cat $infile | tr -d ',' | tr -d '"' | tr '\t' ',' > $csv_file
rm $infile

echo "TIMEDATE CONVERSION"

../py_scripts/timedate.py -f $csv_file -s space -c 2
mv $tmp_file $csv_file

## Clean up problematic characters
## grep -Eo '[^A-Za-z0-9.(), -]' $csv_file | sort | uniq -c | sort
# characters found: ; ^ * { } ' / _ |     & >

echo "FIXING PROBLEMATIC CHARACTERS"
cat $csv_file | tr '_' '.' | tr -d "'" | tr ';' ' ' | tr '|' ' ' | tr '{' '(' \
| tr '}' ')' | tr "^" "-" | tr '*' '-' | tr '/' '-' > $tmp_file
mv $tmp_file $csv_file

sed -i 's/&/and /g' $csv_file
sed -i 's/>/above /g' $csv_file

## Convert all blank fields to "NULL"
echo "CONVERTING BLANKS TO NULLS"
../py_scripts/blanks_to_nulls.py -f $csv_file
mv $tmp_file $csv_file

## Fix miscellaneous surgery problems
../py_scripts/surgery_fixes.py -f $csv_file
mv $tmp_file $csv_file
