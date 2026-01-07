# check if some values in the 'key' column of a CSV file are duplicated
# v1.0 2025-09-22 initial version, reads a filename from command line
# v1.1 2026-01-07 include a list of the files using the dictionary, run automatically

# Result January 2026:

# (v13) PS D:\archive\github\timeline\db> python .\check_duplicates.py
# Usage: python check_duplicates.py <filename.csv>
# Files using dictionary:
#  - adam-moses.csv - ✅  No duplicates found in 'key' column.
#  - books.csv -  ⚠️ Duplicate keys found:
# Duplicate key 'Ezra' found on lines: [3, 7]
# Duplicate key 'Nehemiah' found on lines: [4, 8]
#  - caesars.csv - ✅  No duplicates found in 'key' column.
#  - events.csv - ✅  No duplicates found in 'key' column.
#  - events_objects.csv - ✅  No duplicates found in 'key' column.
#  - events25.csv - ✅  No duplicates found in 'key' column.
#  - judges.csv - ✅  No duplicates found in 'key' column.
#  - kings.csv -  ⚠️ Duplicate keys found:
# Duplicate key 'Ahaziah' found on lines: [10, 33]
#  - objects.csv - ✅  No duplicates found in 'key' column.
#  - people.csv - ✅  No duplicates found in 'key' column.
#  - periods.csv -  ⚠️ Duplicate keys found:
# Duplicate key 'wilderness' found on lines: [2, 4]
# Duplicate key 'timespan_judges' found on lines: [3, 5]
# Duplicate key 'ww1' found on lines: [12, 27]
# Duplicate key 'ww2' found on lines: [13, 28]
# Duplicate key '30_year_war' found on lines: [14, 25]
#  - prophets.csv - ✅  No duplicates found in 'key' column.
#  - terah-family4.csv -  ⚠️ Duplicate keys found:
# Duplicate key 'Nahor' found on lines: [12, 118]
#  - terah-footnotes4.csv - ✅  No duplicates found in 'key' column.

# All as intended. 
# Number 1, 2, 4, 5, 6, 7, and 8 are printed twice on the timeline, so no problem.
# Number 3 (Ahaziah) and number 9 (Nahor) are the same name for different people, so no problem.

import csv
import sys
from collections import defaultdict

files_using_dictionary = [
    "adam-moses.csv",
    "books.csv",
    "caesars.csv",
    "events.csv",
    "events_objects.csv",
    "events25.csv",
    "judges.csv",
    "kings.csv",
    "objects.csv",
    "people.csv",
    "periods.csv", # this one is special, it uses both key and text_center 
    "prophets.csv",
    "terah-family4.csv",
    "terah-footnotes4.csv" # the values in the dictionary add a "_fn" suffix
]

def find_duplicates(filename):
    duplicates = defaultdict(list)
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if 'key' not in reader.fieldnames:
                print("Error: 'key' column not found in CSV.")
                return

            for i, row in enumerate(reader, start=2):  # start=2 to account for header line
                key_value = row['key']
                duplicates[key_value].append(i)

        # Report duplicates
        found = False
        for key, lines in duplicates.items():
            if len(lines) > 1:
                if not found:
                    print(" ⚠️ Duplicate keys found:")
                found = True
                print(f"Duplicate key '{key}' found on lines: {lines}")
        if not found:
            print("✅  No duplicates found in 'key' column.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_duplicates.py <filename.csv>")
        print("Files using dictionary:")
        for f in files_using_dictionary:
            print(f" - {f} - ", end="")
            find_duplicates(f)
    else:
        find_duplicates(sys.argv[1])
