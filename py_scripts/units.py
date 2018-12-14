#!/usr/bin/env python

import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Converts units for consistency")
    parser.add_argument("-f", "--filename", help="name of file",
                        required=True, type=str)
    return parser.parse_args()


def main():
    args = get_arguments()
    # Use original filename & path to build output filename & path
    newfile = args.filename.split("/")
    newfile[-1] = 'tmp_' + newfile[-1]
    newfile = '/'.join(newfile)
    # Unit conversion dictionary
    unit_dict = {
        "cfu/ml": "cfu/mL",
        "Cfu/ml": "cfu/mL",
        "Cfu/mL": "cfu/mL",
        "CFU/mL": "cfu/mL",
        "copies/ml": "copies/mL",
        "Copies/mL": "copies/mL",
        "DNA Copies/mL": "copies/mL",
        "DNA copies/mL": "copies/mL",
        "copies/ mL": "copies/mL",
        "cpy/mL": "copies/mL",
        "cpy/ml": "copies/mL",
        "g/24hrs": "g/24hr",
        "g/24 h": "g/24hr",
        "g/col.time": "g/ col time",
        "g/col. time": "g/ col time",
        "EIA units": "eia units",
        "EIA Units": "eia units",
        "Index": "index",
        "Lines/Intensity": "lines/intensity",
        "TITER": "titer",
        "Titer": "titer",
        "ug/spec": "ug/specimen",
        "mcg/spec": "ug/specimen",
        "ug/mLFEU": "ug/mL FEU",
        "u/mL": "U/mL",
        "Weeks": "weeks",
        "mL/min/1.73m2": "mL/min/1.73 m2",
        "MEQ/L": "mEq/L",
        "MIU/ML": "mIU/mL",
        "mIU/ml": "mIU/mL",
        "MG/24 HR": "mg/24hr",
        "mg/24hr": "mg/24hr",
        "ngmLhr": "ng/mL/hr",
        "Ratio": "ratio",
        "RATIO": "ratio",
        "Watts": "watts",
        "W": "watts",
        "MM": "mm",
        "mU/l": "mU/L",
        "ML/MIN/MM HG/L": "mL/min/mmHg/L",
        "ml/min/mmHg/L": "mL/min/mmHg/L",
        "mL/mHg/min/L": "mL/min/mmHg/L",
        "mOsm/kgH20": "mOsm/kgH2O",
        "mOsm/kg H20": "mOsm/kgH2O",
        "mOsm/Kg H2O": "mOsm/kgH2O",
        "IntUnit/L": "IU/L",
        "ml/min/mmHg": "mL/min/mmHg",
        "ML/MIN/MM HG": "mL/min/mmHg",
        "mL/mmHg/min": "mL/min/mmHg",
        "mcg/L": "ug/L",
        "AU/ml": "AU/mL",
        "percent Saturation": "percent O2 sat",
        "percent O2 Sat.": "percent O2 sat",
        "cu mm": "mm3",
        "mg/gm": "mg/g",
        "M/mme3": "M/mme",
        "M/cu mm": "M/mm3",
        "M/mme": "M/mm3",
        "/cu mm": "/mm3",
        "HR": "hr",
        "hours": "hr",
        "h": "hr",
        "hrs": "hr",
        "Hr": "hr",
        "K/mme3": "K/mm3",
        "k/cu mm3": "K/mm3",
        "k/cu mm": "K/mm3",
        "K/cu mm": "K/mm3",
        "Liters": "L",
        "ml": "mL",
        "ML": "mL",
        "MM/HR": "mm/hr",
        "L/S": "L/sec",
        "IU/ml": "IU/mL",
        "IU/ML": "IU/mL",
        "10e6 / uL": "10e6/uL",
        "x10(6)/mcL": "10e6/uL",
        "X10 6/uL": "10e6/uL",
        "X106e": "10e6/uL",
        "X106": "10e6/uL",
        "106/uL": "10e6/uL",
        "mg/l": "mg/L",
        "ug/dl": "ug/dL",
        "mcg/dL": "ug/dL",
        "MCG/DL": "ug/dL",
        "NG/DL": "ng/dL",
        "ng/dl": "ng/dL",
        "ug/ml": "ug/mL",
        "UG/ML": "ug/mL",
        "mcg/mL": "ug/mL",
        "MCG/ML": "ug/mL",
        "pg/ml": "pg/mL",
        "PG/ML": "pg/mL",
        "uIU/ml": "uIU/mL",
        "UIU/ML": "uIU/mL",
        "mcIntUnit/mL": "uIU/mL",
        "mcIU/mL": "uIU/mL",
        "BPM": "bpm",
        "EHRLICH UNITS": "ehrlich units",
        "EHRLICH": "ehrlich units",
        "EU": "ehrlich units",
        "Units/mL": "U/mL",
        "unit/mL": "U/mL",
        "U/ml": "U/mL",
        "mcmol/L": "umol/L",
        "deg": "degrees",
        "seconds": "sec",
        "Seconds": "sec",
        "SEC": "sec",
        "sec.": "sec",
        "10e3 / uL": "10e3/uL",
        "x10 3/UL": "10e3/uL",
        "x103/uL": "10e3/uL",
        "X10 3/uL": "10e3/uL",
        "X10 3/ul": "10e3/uL",
        "x10(3)/mcL": "10e3/uL",
        "X103e": "10e3/uL",
        "X103": "10e3/uL",
        "10X3": "10e3/uL",
        "X10 3": "10e3/uL",
        "103/uL": "10e3/uL",
        "MM HG": "mmHg",
        "mmHG": "mmHg",
        "NG/ML": "ng/mL",
        "ng/ml": "ng/mL",
        "/LPF": "/lpf",
        "LPF": "/lpf",
        "ml/min": "mL/min",
        "/HPF": "/hpf",
        "HPF": "/hpf",
        "U / L": "U/L",
        "Units/L": "U/L",
        "fl": "fL",
        "G/DL": "g/dL",
        "g/dl": "g/dL",
        "gm/dL": "g/dL",
        "mmol/24hrs": "mmol/24hr",
        "MMOL/L": "mmol/L",
        "mMOL/L": "mmol/L",
        "MG/DL": "mg/dL",
        "mg/dl": "mg/dL"
    }
    # Open original file to edit write changes in new file
    with open(args.filename, "r") as input, open(newfile, "w") as out:
        for line in input:
            line = line.split(",")
            unit = line[14]
            if(unit in unit_dict):
                # print("Old unit " + unit)
                line[14] = unit_dict[unit]
                # print("new Unit " + line[14])
            line = ",".join(line)
            out.write(line)


if __name__ == "__main__":
    main()
