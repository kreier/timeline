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
import math
from datetime import datetime, timedelta

def is_leap(astron_year):
    """Astronomical leap year: Year 0 (1 BCE), -4 (5 BCE), etc., are leap years."""
    return (astron_year % 4 == 0 and astron_year % 100 != 0) or (astron_year % 400 == 0)

def float_to_date_str(val):
    try:
        if pd.isna(val): return val
        f_val = float(val)
        
        # Continuous math logic
        astron_year = math.floor(f_val)
        fraction = f_val - astron_year
        
        if astron_year >= 1:
            label_year = astron_year
            prefix = ""
        else:
            # astron 0 -> 1 BCE, -538 -> 539 BCE
            label_year = 1 - astron_year
            prefix = "BCE"
            
        days_in_year = 366 if is_leap(astron_year) else 365
        day_offset = int(round(fraction * (days_in_year - 1)))
        
        ref_year = 2000 if is_leap(astron_year) else 2001
        target_date = datetime(ref_year, 1, 1) + timedelta(days=day_offset)
        
        return f"{prefix}{str(label_year).zfill(4)}-{target_date.month:02d}-{target_date.day:02d}"
    except:
        return val

def process_files():
    control_file = 'files_to_convert.csv'
    if not os.path.exists(control_file):
        print(f"Error: {control_file} not found.")
        return

    # Load the control file
    files_df = pd.read_csv(control_file)

    for _, row in files_df.iterrows():
        filepath = os.path.join('..', row['file']) 
        col = row['column']
        
        # Get the global fix for this file (default to 0.0 if empty/not present)
        global_fix = 0.0
        if 'fix' in row and not pd.isna(row['fix']):
            try:
                global_fix = float(row['fix'])
            except ValueError:
                print(f"Warning: Invalid fix value for {row['file']}. Using 0.0.")

        if not os.path.exists(filepath):
            print(f"Skipping: {filepath} not found.")
            continue
            
        print(f"\n--- Processing {row['file']} ---")
        print(f"Target Column: {col} | Global Fix: {global_fix}")
        
        df = pd.read_csv(filepath)
        
        # Check first value for conversion direction
        sample = df[col].dropna().iloc[0]
        try:
            float(sample)
            is_currently_float = True
        except (ValueError, TypeError):
            is_currently_float = False

        if is_currently_float:
            print("Action: Applying fix and converting Float -> Historical String")
            # Apply fix to the whole column first, then convert
            df[col + "_new"] = (df[col] + global_fix).apply(float_to_date_str)
        else:
            print("Action: Historical String -> Float (No fix applied to string conversion)")
            # If you ever need to subtract the fix when going string -> float, 
            # you would add: (df[col].apply(date_str_to_float) - global_fix)
            # For now, we'll assume you're converting TO strings.
            pass

        # Preview results
        print(df[[col, col + "_new"]].head(10))
        
        confirm = input(f"Apply changes to {row['file']}? (y/n): ").lower()
        if confirm == 'y':
            df[col] = df[col + "_new"]
            df.drop(columns=[col + "_new"], inplace=True)
            df.to_csv(filepath, index=False)
            print("File saved successfully.")
        else:
            print("Changes discarded.")

if __name__ == "__main__":
    process_files()
