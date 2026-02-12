import pandas as pd
import os
import math
from datetime import datetime, timedelta

def is_leap(astron_year):
    """Sequence: ... -4, 0 (1 BCE), 4 ... are leaps in proleptic Gregorian."""
    return (astron_year % 4 == 0 and astron_year % 100 != 0) or (astron_year % 400 == 0)

def float_to_date_str(val):
    try:
        if pd.isna(val): return val
        f_val = float(val)
        
        # 1. Start of astronomical year
        astron_year = math.floor(f_val)
        fraction = f_val - astron_year
        
        # 2. Map to Historical Labels
        if astron_year >= 1:
            label_year = astron_year
            prefix = ""
        else:
            label_year = 1 - astron_year
            prefix = "BCE"
            
        days_in_year = 366 if is_leap(astron_year) else 365
        day_offset = int(round(fraction * (days_in_year - 1)))
        
        # 3. Determine Month/Day
        ref_year = 2000 if is_leap(astron_year) else 2001
        target_date = datetime(ref_year, 1, 1) + timedelta(days=day_offset)
        
        return f"{prefix}{str(label_year).zfill(4)}-{target_date.month:02d}-{target_date.day:02d}"
    except:
        return val

def date_str_to_float(val):
    try:
        if pd.isna(val): return val
        s = str(val).strip().upper()
        
        # Parse BCE and Year
        is_bce = "BCE" in s
        clean_s = s.replace("BCE", "")
        if clean_s.startswith("-"): # Handle legacy negative strings
            is_bce = True
            clean_s = clean_s[1:]
            
        parts = clean_s.split('-')
        if len(parts) != 3: return 0.0
        
        label_year = int(parts[0])
        month, day = int(parts[1]), int(parts[2])
        
        # Convert back to Astronomical Coordinate
        astron_year = label_year if not is_bce else 1 - label_year
            
        days_in_year = 366 if is_leap(astron_year) else 365
        ref_year = 2000 if is_leap(astron_year) else 2001
        day_of_year = (datetime(ref_year, month, day) - datetime(ref_year, 1, 1)).days
        
        return float(astron_year) + (day_of_year / days_in_year)
    except:
        return 0.0

def run_test_suite():
    tests = [
        (2024.75, "2024-10-01", "Modern Oct"),
        (-537.25, "BCE0539-10-01", "Babylon Oct (Coordinate -537.25)"),
        (0.5, "BCE0001-07-02", "Midway 1 BCE"),
        (1.5, "0001-07-02", "Midway 1 CE")
    ]
    
    print(f"{'Float':<10} | {'Result':<15} | Symmetry")
    print("-" * 45)
    for f_in, expected, desc in tests:
        res = float_to_date_str(f_in)
        back = date_str_to_float(res)
        # Check symmetry (within 2 days tolerance for float precision)
        status = "✅" if abs(back - f_in) < 0.01 else f"❌ ({back:.2f})"
        print(f"{f_in:<10} | {res:<15} | {status} ({desc})")

if __name__ == "__main__":
    run_test_suite()
