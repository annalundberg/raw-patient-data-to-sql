#!/bin/bash


echo "CONVERTING FROM CSV TO TSV FOR PROCESSING"
#Convert the original file to a tsv, also remove the one row without a patient ID
Rscript ../r_scripts/flow_to_tsv.R

# Set Files
data_path="<path_to_datafiles>"
infile=$data_path"/data/flow.tsv"
csv_file=$data_path"/data/cleaned_flow.csv"
tmp_file=$data_path"/data/tmp_cleaned_flow.csv"

echo "REFORMATTING CHARACTERS, CONVERTING BACK TO CSV"
# remove ',' and '"' to allow processing as a csv later
cat $infile | tr ',' ' ' | tr -d '"' | tr '\t' ',' > $csv_file
rm $infile

echo "CONVERT TIME AND DATE TO SMALLTIMEDATE FORMAT"
../py_scripts/timedate.py -f $csv_file -s space -c 3 -c 4
mv $tmp_file $csv_file

## Clean up problematic characters
## grep -Eo '[^A-Za-z0-9.(), -]' cleaned_results.csv | sort | uniq -c | sort
echo "FIXING PROBLEMATIC CHARACTERS"
cat $csv_file | tr '_' ' ' | tr -d '?' | tr -d "'" | tr ';' ' ' | tr -d '$' | tr "+" " " | \
tr -d "\*" | tr "=" " " > $tmp_file
mv $tmp_file $csv_file

sed -i 's/>/above /g' $csv_file
sed -i 's/#/NUMBER/g' $csv_file
sed -i 's/%/percent/g' $csv_file

## Convert all blank fields to "NULL"
echo "CONVERTING BLANKS TO NULLS"
../py_scripts/blanks_to_nulls.py -f $csv_file
mv $tmp_file $csv_file
