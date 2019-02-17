# raw-patient-data-to-sql
## Extract-Transform-Load
Converting raw patient data from excel/csv files into sql database compatible tables.  
Includes standardizing formats and data cleaning.  
Input files are not publicly available but are anonymized .csv versions of:  
- Patient Flowsheets
- Lab Results
- Patient Demographics
- Hospitalizations Records
- Visit Records
- Surgery Records
- Tissue Sample Staging Records

## The Transform Pipeline
Each raw csv was processed through a pipeline contained in main scripts.  
Each main script is written in Bash and uses scripts contained in the R_scripts and/or py_scripts folders.  
To apply pipeline to datafiles, edit the filepaths in mainscript any R_scripts used.

## Load  
The main script folder also contains a psql script used to build a database from the cleaned files.

## The Poster
- PDF version available
- Project References
- Supplemental
