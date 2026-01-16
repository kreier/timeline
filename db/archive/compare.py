# Compare two dictionaries for their entries in column key, english and notes
# The two arguments are the two languages to compare
#
# Structure: 
#  Google docs:    key, text, english, notes - current_key, current_text, current_english, current_notes
#  dictionary csv: key, text, english, notes 
#  reference csv:  key,          text, version, notes
#  reference dictionary: key, text, alternative, notes
#
# 2026-01-16 outdated:
#  Google docs:              key, text, english, notes, tag, checked
#  dictionary csv:           key, text, english, notes, tag, checked
#  dictionary_reference.csv: key, v, english, notes, tag

import sys
import pandas as pd

def compare_reference(language1):
    print(f"Comparing size of {language1} with reference dictionary: ", end="")
    try:
        # Importing the reference dictionary
        reference_file = "../db/dictionary_reference.csv"
        reference_dict = pd.read_csv(reference_file).fillna(" ")

        # Importing the specific language dictionary
        language_file = f"../db/dictionary_{language1}.csv"
        language_dict = pd.read_csv(language_file).fillna(" ")

        # Comparing the "key" columns
        reference_keys = set(reference_dict["key"])
        language_keys = set(language_dict["key"])

        # Find matching and non-matching keys
        matches = reference_keys.intersection(language_keys)
        differences = reference_keys.difference(language_keys)

        # print(f"Matches between reference and {language1}: {matches}")
        print(f"{len(matches)} matching keys found.")
        if len(differences) > 0:
            print(f"\nNumber of non-matching entries: {len(differences)}")
            print(f"Non-matching entries: {differences}")
        else:
            print("All entries match with the reference dictionary.")
        
        # Ensure both files have the required columns

        if "text" not in reference_dict.columns or "english" not in language_dict.columns:
            print("Error: Missing 'text' or 'english' column in one of the dictionaries.")
            return
        
        differences = []   # To store differences in text and english columns

        # Iterate through each line of the language file

        for i in range(len(language_dict)):
            reference_text = reference_dict.loc[i, "text"]
            language_text = language_dict.loc[i, "english"]

            if reference_text != language_text:
                differences.append((i+1, language_dict["key"][i], reference_text, language_text))

        # Output the differences

        if differences:
            print("\nDifferences found:")
            for line in differences:
                print(f"Line {line[0]}: Key '{line[1]}' - Reference: '{line[2]}' vs Language: '{line[3]}'")
        else:
            print("No differences found.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the files exist and paths are correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

def compare(language1, language2):
    print(f"Comparing {language1} with {language2}.")

def main():
    # Get the command line arguments
    args = sys.argv[1:] # Skip the first argument (the script name)

    if len(args) == 1:
        language1 = args[0]
        compare_reference(language1)
    # If two arguments are provided, compare the two languages
    elif len(args) == 2:
        language1 = args[0]
        language2 = args[1]
        compare(language1, language2)
    else:
        print("Usage: python compare.py <language1> [<language2>]")
        print("If only one language is provided, it will be compared to a reference language.")

if __name__ == "__main__":
    main()
