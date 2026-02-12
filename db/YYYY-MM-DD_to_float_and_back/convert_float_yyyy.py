# This time with Gemini 3
#
# Prompt for Pro:
#
# I have a few csv files with date values in float and explicit YYYY-MM-DD 
# format and want to convert them. The files are listed in a files_to_convert.csv 
# with 'file' given the file name and 'column' given the column in this file 
# where the date is found. All respective data files are one folder above in 
# the hierachy. Create a convert_float_yyyy.py program that opens the respective 
# csv files one after another, investigates the column to decide which format 
# it is, creates a conversion and show it. When the user agrees, it writes the 
# converted value back to the csv file. Please use pandas. The date can be in 
# float or the YYYY-MM-DD format. For dates BCE it is either negative or in the 
# style BCEYYYY-MM-DD format. Convert both ways automatically after determining 
# what type is present.

import pandas as pd
import os
from datetime import datetime, timedelta

def is_leap(year):
    # Standard leap year check for the magnitude of the year
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def float_to_date_str(val):
    """
    Converts Mathematical Float to Historical String.
    Example: -538.79 (Oct 539 BCE) -> 'BCE0539-10-15'
    """
    try:
        if pd.isna(val): return val
        f_val = float(val)
        
        # Determine astronomical year and fraction
        astron_year = int(f_val) if f_val >= 0 else int(f_val) - (1 if f_val % 1 != 0 else 0)
        # Note: we floor the negative float to get the start of the astronomical year
        import math
        astron_year = math.floor(f_val)
        fraction = f_val - astron_year
        
        # Convert Astronomical Year to Historical Label
        if astron_year >= 1:
            prefix = ""
            label_year = astron_year
        else:
            # 0 -> 1 BCE, -1 -> 2 BCE, -538 -> 539 BCE
            prefix = "BCE"
            label_year = abs(astron_year - 1)
            
        days_in_year = 366 if is_leap(label_year) else 365
        day_offset = int(round(fraction * days_in_year))
        
        # Use a reference year to get Month/Day
        ref_year = 2000 if is_leap(label_year) else 2001
        target_date = datetime(ref_year, 1, 1) + timedelta(days=day_offset)
        
        return f"{prefix}{str(label_year).zfill(4)}-{target_date.month:02d}-{target_date.day:02d}"
    except:
        return val

def date_str_to_float(val):
    """
    Converts Historical String to Mathematical Float.
    Example: 'BCE0539-10-15' -> -538.79
    """
    try:
        if pd.isna(val): return val
        s = str(val).strip().upper()
        
        is_bce = False
        if s.startswith("BCE"):
            is_bce = True
            s = s.replace("BCE", "")
        elif s.startswith("-"):
            is_bce = True
            s = s.replace("-", "")
            
        parts = s.split('-')
        label_year = int(parts[0])
        month, day = int(parts[1]), int(parts[2])
        
        # Convert Historical Label to Astronomical Year
        if is_bce:
            astron_year = -(label_year - 1)
        else:
            astron_year = label_year
            
        days_in_year = 366 if is_leap(label_year) else 365
        ref_year = 2000 if is_leap(label_year) else 2001
        day_of_year = (datetime(ref_year, month, day) - datetime(ref_year, 1, 1)).days
        
        return astron_year + (day_of_year / days_in_year)
    except:
        return val

def process_files():
    if not os.path.exists('files_to_convert.csv'):
        print("Control file not found.")
        return

    files_df = pd.read_csv('files_to_convert.csv')

    for _, row in files_df.iterrows():
        filepath = os.path.join('..', row['file'])
        col = row['column']
        
        if not os.path.exists(filepath): continue
        df = pd.read_csv(filepath)
        
        # Check first value for type
        sample = df[col].dropna().iloc[0]
        try:
            float(sample)
            is_num = True
        except:
            is_num = False

        if is_num:
            print(f"Converting {row['file']} [{col}] to String...")
            df[col + "_converted"] = df[col].apply(float_to_date_str)
        else:
            print(f"Converting {row['file']} [{col}] to Float...")
            df[col + "_converted"] = df[col].apply(date_str_to_float)

        print(df[[col, col + "_converted"]].head())
        if input("Save? (y/n): ").lower() == 'y':
            df[col] = df[col + "_converted"]
            df.drop(columns=[col + "_converted"], inplace=True)
            df.to_csv(filepath, index=False)

if __name__ == "__main__":
    process_files()
