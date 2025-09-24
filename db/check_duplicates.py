import csv
import sys
from collections import defaultdict

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
                found = True
                print(f"Duplicate key '{key}' found on lines: {lines}")
        if not found:
            print("No duplicates found in 'key' column.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_duplicates.py <filename.csv>")
    else:
        find_duplicates(sys.argv[1])
