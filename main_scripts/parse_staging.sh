#!/usr/bin/env bash

## Pipeline for Staging csv cleaning ##

echo "SET FILES"
# Files
data_path="<path_to_datafile>" ##edit this to your data folder
infile=$data_path"/staging.tsv"
hyperlink=$data_path"/stag_link.tsv"
csv_file=$data_path"/final_data/cleaned_staging.csv"
tmp_file=$data_path"/final_data/tmp_cleaned_staging.csv"

echo "CONVERTING FROM CSV TO TSV FOR PROCESSING"
## Convert the original file to a tsv and separtes out hyperlink column
Rscript ./r_scripts/stag_to_tsv.R

echo "CONVERT IMG HYPERLINK TO IMG ID"
## Reincorporate image ID in place of hyperlink
echo 'snapshot_id' > $data_path/stag_img_id.tsv
cat $data_path/stag_link.tsv | sed -nE 's/^.*?snapshotId=([0-9]+).*$/\1/gp' \
>> $data_path/stag_img_id.tsv
rm $data_path/stag_link.tsv

echo "ADD IMG ID COLUMN TO STAGING TSV"
Rscript ./r_scripts/stag_resorb.R
rm $data_path/stag_img_id.tsv

echo "REFORMATTING CHARACTERS, CONVERTING BACK TO CSV"
# remove ',' and '"' to allow processing as a csv later
cat $infile | tr -d ',' | tr -d '"' | tr '\t' ',' > $csv_file
rm $infile

echo "FIXING PROBLEMATIC CHARACTERS"
## Clean up problematic characters

#grep -Eo '[^A-Za-z0-9.(), -]' $csv_file | sort | uniq -c | sort -n -r
# Found ` ^ < = > _ : ? / " [ ] * % +

cat $csv_file | tr -d '`' > $tmp_file
mv $tmp_file $csv_file

cat $csv_file | tr '_' '.' | tr -d '"' | tr -d '?' | tr ':' ' ' | tr '[' '(' \
| tr ']' ')' | tr "^" "-" | tr '*' '-' | tr '/' '-' > $tmp_file
mv $tmp_file $csv_file

sed -i 's/</below /g' $csv_file
sed -i 's/>/above /g' $csv_file
sed -i 's/%/ percent/g' $csv_file  ##potentially could be removed instead
sed -i 's/+/(plus)/g' $csv_file


echo "CONVERTING BLANKS TO NULLS"
## Convert all blank fields to "NULL"
./py_scripts/blanks_to_nulls.py -f $csv_file
mv $tmp_file $csv_file


echo "REMOVING DEMOGRAPHIC COLUMNS"
## Remove demographic columns (redundant)
cat $csv_file | cut -d ',' -f 2,3 --complement > $tmp_file
mv $tmp_file $csv_file


echo "REMOVING ILLOGICAL DATA"
## Remove illogical data (negative age)
./py_scripts/fix_age_staging.py -f $csv_file
mv $tmp_file $csv_file


echo "COLLAPSING REDUNDANT CATEGORIES"
## Collapse redundant categories (e.g multiple versions of NULL or upper/lower case)
./py_scripts/staging_collapse_data.py -f $csv_file -c 6 -c 7 -c 8 -c 9 -c 10 \
-c 12 -c 13 -c 14 -c 15 -c 16 -c 22 -c 25 -c 27 -c 28 -c 29
mv $tmp_file $csv_file
