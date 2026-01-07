# Dictionary coverage check
#
# The entries in the dictionary_XX connect the key value with the text. 
# The same row also has english as reference and for comparison. And notes for more details.
#
# The dictonary files are used by the following files and will be checked if some of the keys are never used:

import pandas as pd

# Load dictionary reference
dict_df = pd.read_csv("../db/dictionary_reference.csv")
dict_keys = set(dict_df['key'].astype(str))

files_using_dictionary = [
    "../db/adam-moses.csv",
    "../db/books.csv",
    "../db/caesars.csv",
    "../db/events.csv",
    "../db/events_objects.csv",
    "../db/events25.csv",
    "../db/judges.csv",
    "../db/kings.csv",
    "../db/objects.csv",
    "../db/people.csv",
    "../db/periods.csv", # this one is special, it does not use key but text_left, text_center and text_right
    "../db/prophets.csv",
    "../db/terah-family4.csv",
    "../db/terah-footnotes4.csv", # the values in the dictionary add a "_fn" suffix
    "../db/internal_keys.csv"
]

def clean_keys(series):
    """Convert to string, strip whitespace, drop blanks and NaN."""
    return set(
        series.dropna()
              .astype(str)
              .str.strip()
              .replace("", pd.NA)
              .dropna()
    )

all_keys = set()

for file in files_using_dictionary:
    df = pd.read_csv(file)
    
    if file.endswith("periods.csv"):
        keys = clean_keys(df['text_left']) | \
               clean_keys(df['text_center']) | \
               clean_keys(df['text_right'])
    elif file.endswith("terah-footnotes4.csv"):
        keys = {f"{k}_fn" for k in clean_keys(df['key'])}
    else:
        keys = clean_keys(df['key'])
    
    all_keys |= keys

# Compare

missing_keys = dict_keys - all_keys
extra_keys = all_keys - dict_keys

print(f"Missing keys (in dictionary but not used): {len(missing_keys)}\n", missing_keys)
print(f"Extra keys (used but not in dictionary): {len(extra_keys)}\n", extra_keys)
