# raw-patient-data-to-sql

Converting raw patient data from excel/csv files into sql database compatible tables.  
Includes standardizing formats and data cleaning.  
Input files are not publicly available but are anonymized .csv versions of:  
- Patient Flowsheets
- Lab Results
- Patient Demographics
- Hospitalizations Records
- Visit Records
- Surgery Records

## The Pipeline
Each raw csv was processed through a pipeline contained in main scripts.  
Each main script is written in Bash and uses scripts contained in the R_scripts and/or py_scripts folders.  
To apply pipeline to datafiles, edit the filepaths in mainscript any R_scripts used.
