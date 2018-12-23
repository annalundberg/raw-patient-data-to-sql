#!/usr/bin/env bash

echo "CONVERTING FROM CSV TO TSV FOR PROCESSING"

#Convert the original file to a tsv, also remove the one row without a patient ID
Rscript ../r_scripts/visits_to_tsv.R

# Files
data_path="<path_to_datafiles>"
infile=$data_path"/data/visits.tsv"
csv_file=$data_path"/data/cleaned_visits.csv"
tmp_file=$data_path"/data/tmp_cleaned_visits.csv"

echo "REFORMATTING CHARACTERS, CONVERTING BACK TO CSV"

# remove ',' and '"' to allow processing as a csv later
cat $infile | tr -d ',' | tr -d '"' | tr '\t' ',' > $csv_file
rm $infile

echo "TIMEDATE CONVERSION"

../py_scripts/timedate.py -f $csv_file -s space -c 2
mv $tmp_file $csv_file

echo "REMOVING OUTLIERS"

../py_scripts/remove_outliers.py -f $csv_file
mv $tmp_file $csv_file

## Clean up problematic characters
## grep -Eo '[^A-Za-z0-9.(), -]' $csv_file | sort | uniq -c | sort
# characters found: ; | ' ^ % + _ : /

echo "FIXING PROBLEMATIC CHARACTERS"
cat $csv_file | tr '_' '.' | tr -d "'" | tr ';' ' ' | tr '|' ' ' \
| tr "^" "-" | tr '/' '-' > $tmp_file
mv $tmp_file $csv_file

# characters to still deal with: + %
sed -i 's/+/(plus) /g' $csv_file
sed -i 's/%/percent/g' $csv_file
sed -i 's/NA/NULL/g' $csv_file

## Convert all blank fields to "NULL"
echo "CONVERTING BLANKS TO NULLS"
../py_scripts/blanks_to_nulls.py -f $csv_file
mv $tmp_file $csv_file

echo "CONVERTING TO METRIC MEASURES OF HEIGHT AND WEIGHT"

../py_scripts/convert_to_metric.py -f $csv_file -c 3 -u oz -c 4 -u inch
mv $tmp_file $csv_file
