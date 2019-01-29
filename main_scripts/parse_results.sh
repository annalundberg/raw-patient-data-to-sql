#!/bin/bash

# 73% of the data is accounted for between these tables (346228/474150)

#Sort the whole file
# cut -f 10 -d , cleaned_results.csv | sort | uniq -c | sort -n
# Inspect individual tests
# cut -f 10,11 csv_file | grep "12 LEAD ECG" | sort | uniq | sort

echo "CONVERTING FROM CSV TO TSV FOR PROCESSING"
#Convert the original file to a tsv, also remove the one row without a patient ID
Rscript ../r_scripts/results_to_tsv.R

# Files
data_path="<path_to_datafiles>"
infile=$data_path"/data/results.tsv"
csv_file=$data_path"/data/cleaned_results.csv"
tmp_file=$data_path"/data/tmp_cleaned_results.csv"

echo "REFORMATTING CHARACTERS, CONVERTING BACK TO CSV"
# remove ',' and '"' to allow processing as a csv later
cat $infile | tr ',' ' ' | tr -d '"' | tr '\t' ',' > $csv_file
rm $infile

echo "CONVERTING TIMEDATE TO SMALLTIMEDATE FORMAT"

../py_scripts/timedate.py -f $csv_file -s slash -c 6 -c 7 -c 8
mv $tmp_file $csv_file

echo "REFORMATTING COLUMNS"
##column split conversion script
../py_scripts/column_split.py -f $csv_file -c 11
mv $tmp_file $csv_file

## Convert all blank fields to "NULL"
echo "CONVERTING BLANKS TO NULLS"
./blanks_to_nulls.py -f $csv_file
mv $tmp_file $csv_file


## Clean up problematic characters
## grep -Eo '[^A-Za-z0-9.(), -]' cleaned_results.csv | sort | uniq -c | sort
echo "FIXING PROBLEMATIC CHARACTERS"

cat $csv_file | tr '[' '(' | tr ']' ')' | tr -d '\\' | tr -d '!' | \
tr '_' ' ' | tr -d '?' | tr -d "'" | tr ';' ' ' | tr -d '$' | tr "+" " " \
> $tmp_file

mv $tmp_file $csv_file

sed -i 's/<=/le /g' $csv_file
sed -i 's/>=/le /g' $csv_file
sed -i 's/>/above /g' $csv_file
sed -i 's/</below /g' $csv_file
sed -i 's/#/NUMBER/g' $csv_file
sed -i 's/@/AT/g' $csv_file
sed -i 's/&/AND/g' $csv_file
sed -i 's/%/percent/g' $csv_file
sed -i 's/10\^/10e/g' $csv_file
sed -i 's/mm\^3/mm3/g' $csv_file
sed -i 's/10\*/10e/g' $csv_file
sed -i 's/=//g' $csv_file
sed -i 's/\*//g' $csv_file
sed -i 's/\^//g' $csv_file

## Convert units to a consistent format
## cut -d ',' -f 15 cleaned_results.csv | sort | uniq -c | sort -d -k 2
echo "RENAMING LAB UNITS FOR CONSISTENCY"
../py_scripts/units.py -f $csv_file
mv $tmp_file $csv_file

echo "RENAMING TESTS FOR CONSISTENCY"
# 12 LEAD ECG - 13827
# RENAL PANEL - 25482
sed -i 's/RENAL TX POST PANEL (EXT RESULTS)/RENAL TX POST PANEL/' $csv_file

# URINE MICROSCOPIC EXAM - 18172
sed -i 's/URINE  MICROSCOPIC EXAM/URINE MICROSCOPIC EXAM/' $csv_file

# LEUKOREDUCED RED BLOOD CELLS - 9147
sed -i 's/PRODUCT- RED CELLS LEUKOREDUCED/LEUKOREDUCED RED BLOOD CELLS/' $csv_file
sed -i 's/PRODUCT - RED CELLS LEUKOREDUCED/LEUKOREDUCED RED BLOOD CELLS/' $csv_file
sed -i 's/BLOOD BANK PRODUCT/LEUKOREDUCED RED BLOOD CELLS/' $csv_file
sed -i 's/TRANSFUSE RED CELLS  LEUKOREDUCED/LEUKOREDUCED RED BLOOD CELLS/' $csv_file

# ARTERIAL BLOOD GASES - 11625
sed -i 's/BLOOD GASES  ARTERIAL - LAB/ARTERIAL BLOOD GASES/' $csv_file
sed -i 's/BLOOD GASES  ARTERIAL/ARTERIAL BLOOD GASES/' $csv_file
sed -i 's/ABG-FULL ABL  POC/ARTERIAL BLOOD GASES/' $csv_file
sed -i 's/ARTERIAL BLOOD GAS  POC/ARTERIAL BLOOD GASES/' $csv_file
sed -i 's/ARTERIAL BLOOD GASES IP ONLY/ARTERIAL BLOOD GASES/' $csv_file

# UA DIPSTICK ONLY - 16038
sed -i 's/UA 10 DIP  POC/UA DIPSTICK ONLY/' $csv_file
sed -i 's/CHH - UA  DIPSTICK ONLY/UA DIPSTICK ONLY/' $csv_file
sed -i 's/UA  DIPSTICK ONLY/UA DIPSTICK ONLY/' $csv_file
sed -i 's/UA DIPSTICK ONLY W\/O MICRO  POC/UA DIPSTICK ONLY/' $csv_file
sed -i 's/UA DIPSTICK ONLY  POC/UA DIPSTICK ONLY/' $csv_file
sed -i 's/UA DIPSTICK ONLY  POC RESULT/UA DIPSTICK ONLY/' $csv_file
sed -i 's/UA 10 DIP POC/UA DIPSTICK ONLY/' $csv_file
sed -i 's/UA DIPSTICK 10 DIP W\/O MICRO  POC/UA DIPSTICK ONLY/' $csv_file
sed -i 's/UA DIPSTICK 10 DIP W\/O MICRO (AUTOMATED)  POC/UA DIPSTICK ONLY/' $csv_file
sed -i 's/UA DIPSTICK ONLY RESULT/UA DIPSTICK ONLY/' $csv_file

# RENAL FUNCTION SET - 25482
sed -i 's/RENAL FUNCTION SET (NA K CL CO2 BUN CREAT GLUC CA PHOS ALB )/RENAL FUNCTION SET/' $csv_file
sed -i 's/RENAL FUNCTION SET (BASIC+PO4 ALB)/RENAL FUNCTION SET/' $csv_file

# CBC - 136728
sed -i 's/CBC CELLDYNE ADULT (NO CHG)  POC/CBC/' $csv_file
sed -i 's/CBC W\/DIFF  NO REFLEX/CBC/' $csv_file
sed -i 's/CHH - CBC ONLY W\/PLATELET/CBC/' $csv_file
sed -i 's/CBC ONLY W\/PLATELET/CBC/' $csv_file
sed -i 's/CBC ONLY WITH PLATELET/CBC/' $csv_file
sed -i 's/CBC (HEMOGRAM ONLY)/CBC/' $csv_file
sed -i 's/CBC (HEMOGRAM) ONLY/CBC/' $csv_file
sed -i 's/CBC+DIFF  POC/CBC/' $csv_file
sed -i 's/CBC CELLDYNE ADULT  POC/CBC/' $csv_file
sed -i 's/CHH - CBC AUTODIFF/CBC/' $csv_file
sed -i 's/CBC AND AUTO DIFF/CBC/' $csv_file
sed -i 's/CBC  POC/CBC/' $csv_file
sed -i 's/CBC W\/ AUTO DIFF - CHO/CBC/' $csv_file
sed -i 's/CBC W\/ DIFF  REFLEX/CBC/' $csv_file
sed -i 's/CBC W\/DIFF  REFLEX/CBC/' $csv_file
sed -i 's/CHH - CBC/CBC/' $csv_file
sed -i 's/CHH CBC W DIFFERENTIAL/CBC/' $csv_file
sed -i 's/CBC CELLDYN ADULT (NO CHG)  POC/CBC/' $csv_file
sed -i 's/CBC W\/O PLATELETS/CBC/' $csv_file
sed -i 's/CBC+DIFF POC/CBC/' $csv_file
sed -i 's/CBC CELLDYN ADULT  POC/CBC/' $csv_file
sed -i 's/CBC WITH PLATELET/CBC/' $csv_file
sed -i 's/CBC  PLATELET AND DIFFERENTIAL/CBC/' $csv_file
sed -i 's/CHH - CBC W DIFFERENTIAL/CBC/' $csv_file
sed -i 's/CHH - CBC ONLY/CBC/' $csv_file
sed -i 's/CBC W DIFFERENTIAL/CBC/' $csv_file
sed -i 's/CBC ONLY W\/O PLATELETS/CBC/' $csv_file
sed -i 's/CBC  WITH DIFFERENTIAL/CBC/' $csv_file
sed -i 's/CBC WITH MANUAL DIFFERENTIAL/CBC/' $csv_file
sed -i 's/CBC WITH AUTO DIFF/CBC/' $csv_file
sed -i 's/CBC ONLY/CBC/' $csv_file
sed -i 's/AUTO DIFFERENTIAL/CBC/' $csv_file
sed -i 's/DIFFERENTIAL  ADD ON/CBC/' $csv_file
sed -i 's/MANUAL DIFFERENTIAL - CHO/CBC/' $csv_file
sed -i 's/DIFFERENTIAL/CBC/' $csv_file
sed -i 's/MANUAL DIFFERENTIAL/CBC/' $csv_file
sed -i 's/MANUAL CBC/CBC/' $csv_file
sed -i 's/CBC  BFL/CBC/' $csv_file

# METABOLIC PANEL - 105107
sed -i 's/COMPLETE METABOLIC SET (NA K CL CO2 BUN CREAT GLUC CA AST ALT BILI TOTAL ALK PHOS ALB PROT TOTAL)/METABOLIC PANEL/' $csv_file
sed -i 's/COMPLETE METABOLIC PICCOLO  POC/METABOLIC PANEL/' $csv_file
sed -i 's/CHH - COMPLETE METABOLIC SET/METABOLIC PANEL/' $csv_file
sed -i 's/CMP METABOL POC/METABOLIC PANEL/' $csv_file
sed -i 's/COMP METABOLIC SET/METABOLIC PANEL/' $csv_file
sed -i 's/COMPLETE METABOLIC PANEL - CHO/METABOLIC PANEL/' $csv_file
sed -i 's/CMP  POC (BMP+LFT)/METABOLIC PANEL/' $csv_file
sed -i 's/BASIC METABOLIC SET (NA  K  CL  TCO2  BUN  CR  GLU  CA)/METABOLIC PANEL/' $csv_file
sed -i 's/COMPLETE METABOLIC  POC/METABOLIC PANEL/' $csv_file
sed -i 's/COMPREHENSIVE METABOLIC PAN W\/ GFR/METABOLIC PANEL/' $csv_file
sed -i 's/COMPLETE METABOLIC PICCOLO (NO CHG)  POC/METABOLIC PANEL/' $csv_file
sed -i 's/COMP METABOLIC SET  PLASMA/METABOLIC PANEL/' $csv_file
sed -i 's/COMPLETE METABOLIC PANEL/METABOLIC PANEL/' $csv_file
sed -i 's/COMPLETE METABOLIC SET  PLASMA/METABOLIC PANEL/' $csv_file
sed -i 's/COMPLETE METABOLIC SET (BASIC+ALB ALKP TBIL AST TPRO ALT)/METABOLIC PANEL/' $csv_file
sed -i 's/BASIC METABOLIC SET - CHO/METABOLIC PANEL/' $csv_file
sed -i 's/CHH - BASIC METABOLIC SET/METABOLIC PANEL/' $csv_file
sed -i 's/BASIC METABOLIC SET (NA K CL BUN CR GLU CO2 CA)/METABOLIC PANEL/' $csv_file
sed -i 's/BASIC METABOLIC SET  PLASMA/METABOLIC PANEL/' $csv_file
sed -i 's/BASIC METABOLIC SET (NA  K  CL  HCO3  BUN  CR  GLU  CA)/METABOLIC PANEL/' $csv_file
sed -i 's/METABOLIC PANEL (BASIC+ALB ALKP TBIL AST TPRO ALT)/METABOLIC PANEL/' $csv_file
sed -i 's/METABOLIC PANEL  PLASMA/METABOLIC PANEL/' $csv_file
sed -i 's/METABOLIC PANEL W\/ GFR/METABOLIC PANEL/' $csv_file
sed -i 's/BASIC METABOLIC PANEL/METABOLIC PANEL/' $csv_file
sed -i 's/BASIC METABOLIC SET/METABOLIC PANEL/' $csv_file

echo "WRITING OUTPUT FILES"

# Split the file
grep "METABOLIC PANEL" $csv_file > $data_path"/data/results/metabolic.csv"
grep "LEUKOREDUCED RED BLOOD CELLS" $csv_file > $data_path"/data/results/transfusion.csv"
grep "ARTERIAL BLOOD GASES" $csv_file > $data_path"/data/results/blood_gas.csv"
grep "UA DIPSTICK ONLY" $csv_file > $data_path"/data/results/ua_dip.csv"
grep "RENAL FUNCTION SET" $csv_file > $data_path"/data/results/renal.csv"
grep ",CBC," $csv_file > $data_path"/data/results/cbc.csv"
grep "12 LEAD ECG" $csv_file > $data_path"/data/results/ecg.csv"
grep "URINE MICROSCOPIC EXAM" $csv_file > $data_path"/data/results/ua_micro.csv"

# Everything else to miscellanous tests file
grep -v "METABOLIC PANEL" $csv_file | grep -v "LEUKOREDUCED RED BLOOD CELLS" \
| grep -v "ARTERIAL BLOOD GASES" | grep -v "UA DIPSTICK ONLY" | grep -v "RENAL FUNCTION SET" \
| grep -Ev ",CBC," | grep -v "12 LEAD ECG" | grep -v "URINE MICROSCOPIC EXAM" \
> $data_path"/data/results/misc.csv"

echo "REFORMATTING OUTPUT FILES"

temp_header=$data_path"/data/results/temp_headers.csv"

# Get the headers from the full file and add them back on
head -1 $csv_file > $temp_header
cat $data_path/data/results/metabolic.csv >> $temp_header
mv $temp_header $data_path/data/results/metabolic.csv

head -1 $csv_file > $temp_header
cat $data_path/data/results/transfusion.csv >> $temp_header
mv $temp_header $data_path/data/results/transfusion.csv

head -1 $csv_file > $temp_header
cat $data_path/data/results/blood_gas.csv >> $temp_header
mv $temp_header $data_path/data/results/blood_gas.csv

head -1 $csv_file > $temp_header
cat $data_path/data/results/ua_dip.csv >> $temp_header
mv $temp_header $data_path/data/results/ua_dip.csv

head -1 $csv_file > $temp_header
cat $data_path/data/results/renal.csv >> $temp_header
mv $temp_header $data_path/data/results/renal.csv

head -1 $csv_file > $temp_header
cat $data_path/data/results/cbc.csv >> $temp_header
mv $temp_header $data_path/data/results/cbc.csv

head -1 $csv_file > $temp_header
cat $data_path/data/results/ecg.csv >> $temp_header
mv $temp_header $data_path/data/results/ecg.csv

head -1 $csv_file > $temp_header
cat $data_path/data/results/ua_micro.csv >> $temp_header
mv $temp_header $data_path/data/results/ua_micro.csv

head -1 $csv_file > $temp_header
cat $data_path/data/results/misc.csv >> $temp_header
mv $temp_header $data_path/data/results/misc.csv

## Fix float values in misc table ##
./py_scripts/fixing_misc.py -f $data_path/data/results/misc.csv
mv $data_path/data/results/tmp_misc.csv $data_path/data/results/misc.csv
