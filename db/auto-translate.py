# Create a google translated dictionary as starting point for a new language
# Updated to work with with https://pypi.org/project/googletrans/ 4.0.2 (latest version)
# Usage: python auto-translate.py [language_code]
# Update 2026: check the translation, expand if necessary

# dictionary_reference.csv has 'key', 'text', 'version' and 'notes'
# dictionary_XX.csv has 'key', 'text', 'english', 'notes' and 'checked'

import os, sys, asyncio
import pandas as pd
from googletrans import Translator

def check_existing(language, filename):
    global dict_translated, dict 
    # Check execution location, exit if not in /timeline/db
    if os.getcwd()[-12:].replace("\\", "/") != "/timeline/db":
        print("This script must be executed inside the /timeline/db folder.")
        exit()
    if os.path.isfile(filename):
        print("A file with this name already exists.")
        print(f"Importing existing dictionary_{language}.csv file for comparison...")
        dict_translated = pd.read_csv(filename)
        dict_translated.fillna(" ", inplace=True) # fill empty cells with a space
        dict_translated.to_csv(filename, index=False)

        # Step 1: Compare the number of keys in both dictionaries and report differences
        if len(dict) != len(dict_translated):
            print(f"⚠️ Warning: The number of entries in the reference dictionary ({len(dict)}) and the existing dictionary ({len(dict_translated)}) do not match.")
        else:
            print("✅ The number of entries in both dictionaries match. Both have", len(dict), "entries.")
        # Multiple entries in the dict_translated with the same key?
        duplicates = dict_translated[dict_translated.duplicated(subset=["key"], keep=False)]
        if not duplicates.empty:
            print("⚠️ Warning: There are duplicate keys in the existing dictionary:")
            print(duplicates)
            user_input = input("Do you want to remove duplicate entries? (yes/no): ")
            if user_input.lower() == "yes" or user_input.lower() == "y":
                dict_translated = dict_translated.drop_duplicates(subset=["key"], keep="first")
                print("Updated dict_translated after removing duplicates:")
                print(dict_translated)
                dict_translated.to_csv(filename, index=False)
        

        # Step 2: Find keys that are in dict_translated but not in dict
        extra_keys = set(dict_translated["key"]) - set(dict["key"])
        # Filter dict_translated to show only extra entries
        extra_entries = dict_translated[dict_translated["key"].isin(extra_keys)]
        if not extra_entries.empty:
            print("Extra entries found, will be relabeled as deprecated:")
            print(extra_entries)

            # # Ask user if they want to remove these lines
            # user_input = input("Do you want to remove these extra entries? (yes/no): ")

            # if user_input.lower() == "yes" or user_input.lower() == "y":
            #     dict_translated = dict_translated[~dict_translated["key"].isin(extra_keys)]
            #     print("Updated dict_translated after removal:")
            #     print(dict_translated)
            #     dict_translated.to_csv(filename, index=False)
            # else:
            #     print("No changes made.")
        else:
            print("No extra entries found in the existing dictionary.")


        # Step 3: Check if dict_translated has the required columns
        required_cols = ["key", "text", "english", "notes", "tag", "checked"]
        # Add missing columns to dict_translated
        for col in required_cols:
            if col not in dict_translated.columns:
                dict_translated[col] = " "   # or use None / pd.NA if you prefer
                print(f"Added missing column: {col}")
        # Reorder columns in dict_translated
        dict_translated = dict_translated[required_cols]


        # Step 4: Find keys that are in dict but not in dict_translated
        missing_keys = set(dict["key"]) - set(dict_translated["key"])
        missing_entries = dict[dict["key"].isin(missing_keys)]
        if not missing_entries.empty:
            print("Entries missing in the existing dictionary:")
            print(missing_entries)

            # Ask user if they want to add these lines
            user_input = input("Do you want to add these missing entries? (yes/no): ")
            if user_input.lower() == "yes" or user_input.lower() == "y":
                # Create a DataFrame for missing entries with required columns
                missing_df = missing_entries[['key', 'english']].copy()
                missing_df['english'] = missing_entries['english'].copy()
                missing_df['notes'] = missing_entries['notes'].copy()

                # Append missing entries to dict_translated
                dict_translated = pd.concat([dict_translated, missing_df], ignore_index=True)
                print("Updated dict_translated after adding missing entries:")
                print(dict_translated)
                dict_translated.to_csv(filename, index=False)


        # Step 5: Match the order of entries in dict_translated to match dict
        # Step 5.1: align dict_translated to dict's key order
        aligned = dict_translated.set_index("key").reindex(dict["key"]).reset_index()
        # Step 5.2: find extra rows (keys not in dict)
        extra = dict_translated[~dict_translated["key"].isin(dict["key"])].copy()
        # Step 5.3: mark them as deprecated
        extra.loc[:, "tag"] = "deprecated"
        # Step 5.4: concatenate aligned first, extras at the end
        dict_translated = pd.concat([aligned, extra], ignore_index=True)


        # Step 6: Check entries in the tag column
        print("\nChecking 'tag' column entries in the existing dictionary...")
        # 6.1 Count missing tag entries
        missing_tags = dict_translated["tag"].isna().sum() + (dict_translated["tag"] == "").sum()
        # 6.2 Find mismatches between dict and dict_translated
        merged = dict_translated.merge(dict[["key", "tag"]], on="key", how="left", suffixes=("", "_dict"))
        mismatches = (merged["tag"] != merged["tag_dict"]) & merged["tag_dict"].notna()
        num_mismatches = mismatches.sum()
        print(f"Number of missing tags in dict_translated: {missing_tags}")
        print(f"Number of mismatched tags compared to dict: {num_mismatches}")
        # 6.3 Update dict_translated's tag values to match dict
        if missing_tags > 0 or num_mismatches > 0:
            print("Updating 'tag' values in dict_translated to match the reference dictionary...")
            dict_translated["tag"] = merged["tag_dict"].fillna(dict_translated["tag"])
            print("dict_translated updated with corrected tag values:")
            print(dict_translated.head())
            dict_translated.to_csv(filename, index=False)


        # Step 7: Check entries in the checked column
        print("\nChecking 'checked' column entries in the existing dictionary...")
        # Normalize values: convert strings to booleans
        dict_translated["checked"] = dict_translated["checked"].replace(
            {"TRUE": True, "True": True, "FALSE": False, "False": False, "": False}
        )
        # Count values
        num_true = (dict_translated["checked"] == True).sum()
        num_false = (dict_translated["checked"] == False).sum()
        num_empty = (dict_translated["checked"] == " ").sum()
        num_nan = (dict_translated["checked"].isna()).sum()
        print(f"TRUE values: {num_true}")
        print(f"FALSE values: {num_false}")
        print(f"Empty values: {num_empty}")
        print(f"NaN values: {num_nan}")
        if num_empty > 0 or num_nan > 0:
            print("Filling empty 'checked' values with FALSE...")
            dict_translated["checked"] = dict_translated["checked"].replace(
                {"TRUE": True, "True": True,
                "FALSE": False, "False": False,
                " ": pd.NA, "": pd.NA}
            )
            # Step 2: convert to pandas nullable boolean dtype
            dict_translated["checked"] = dict_translated["checked"].astype("boolean")
            # Step 3: fill missing values with False
            dict_translated["checked"] = dict_translated["checked"].fillna(False)
            print("Updated dict_translated with cleaned 'checked' column:")
            print(dict_translated.head())
        # Ensure column is strictly boolean
        dict_translated["checked"] = dict_translated["checked"].astype(bool)
        dict_translated.to_csv(filename, index=False)

    else:
        print(f"Creating a new dictionary_{language}.csv file.")
        dict_translated = dict[['key', 'english']].copy()   # create a new dictionary, copy columns key and text
        dict_translated['text'] = dict['english'].copy()    # add a column 'english' and fill with 'text' from english dictionary
        dict_translated['notes'] = dict['notes'].copy()     # add a column 'notes' and fill with 'notes' from english dictionary
        dict_translated['tag'] = dict['tag'].copy()         # add a column 'tag' and fill with 'tag' from english dictionary
        dict_translated['checked'] = False                  # add a column 'checked' and fill with False

    # Step 8: Compare known entries and fix them
    # Step 8.1: match all entries with tag 'timespan' and set checked to True
    timespan_mask = dict_translated["tag"] == "timespan"
    dict_translated.loc[timespan_mask, "checked"] = True
    dict_translated.to_csv(filename, index=False)

    # Step 8.2: Fix 'span_ce' entries - overwrite if checked is False

    # Step 8.3: Fix 'span_bce' entries

    # Step 8.4: Fix 'span_bc' entries

    # Step 8.5: Fix 'float' entries

    # Step 8.6: Fix 'wiki' entries

    # It remains:
    # - scripture
    # - A6-A
    # - A6-B
    # - B9
    # - bible
    # - text


def import_reference():
    global dict
    # print("Import reference english dictionary: ", end="")
    dict = pd.read_csv("./dictionary_reference.csv")
    dict.fillna(" ", inplace=True) # fill empty cells with a space
    # print(f"found {len(dict)} entries.")
    # print(dict)

def missing_bc_bce():
    global dict_translated
    # Check if 'bc' and 'bce' entries are missing or if checked is False
    return False
    missing_bc_bce = False
    for tag in ['span_bc', 'span_bce']:
        mask = (dict_translated['tag'] == tag) & ((dict_translated['text'] == "") | (dict_translated['text'].isna()))
        if mask.any():  # If there are any missing entries for this tag
            missing_bc_bce = True
            num_missing = mask.sum()
            print(f"Found {num_missing} missing entries for tag '{tag}'.")

async def translate_bc_bce(language):
    global dict_translated, number_characters
    async with Translator() as translator:
        for tag in ['span_bc', 'span_bce']:
            mask = (dict_translated['tag'] == tag) & ((dict_translated['text'] == "") | (dict_translated['text'].isna()))

async def translate_dictionary(dictionary, language):
    global number_characters
    async with Translator() as translator:
        for index, row in dict_translated.iterrows(): # with 3 columns 'key' 'text' and 'english'
            english_text = row.english
            number_characters += len(str(english_text))
            if not english_text == " ": # it only applies to row 9 where in english is an empty string (unline Vietnamese or Russian)
                # dict_translated.at[index, 'text'] = translator.translate(english_text, src='en', dest=language).text
                result = await translator.translate(english_text, src='en', dest=language)
                dict_translated.at[index, 'text'] = result.text
                # print('.', end='')
                print(f'{index}: {english_text} - {result.text}')
            # if (index + 1) % 40 == 0:
            #     print(f" {index}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You did not provide a language as argument. Put it as a parameter after the program name.")
        exit()
    language = sys.argv[1]
    filename = "./dictionary_" + language + ".csv"
    print(f"You want to translate to {language}.")

    # Create dataframe and import reference dictionary
    dict = pd.DataFrame() # columns 'key', 'text' for english reference and 'notes' to compare, plus 'alternative' (not used)
    import_reference()
    dict_translated = pd.DataFrame() # columns 'key', 'text' for translated, 'english' for reference, 'notes' to compare, 'tag' and 'checked'

    check_existing(language, filename)

    # Prompt possible translation effort
    # Define the tag values we want to check
    tags_to_check = ["text", "bible", "B9", "A6-A", "A6-B", "scripture", "wiki"]
    # Normalize text column: treat NaN and " " as empty
    dict_translated["text"] = dict_translated["text"].replace(" ", "").fillna("")
    # Build counts per tag
    summary = (
        dict_translated[dict_translated["tag"].isin(tags_to_check)]
        .groupby("tag")["text"]
        .agg(
            missing=lambda col: (col == "").sum(),
            existing=lambda col: (col != "").sum()
        )
        .reset_index()
    )
    # Add totals row
    totals = pd.DataFrame({
        "tag": ["TOTAL"],
        "missing": [summary["missing"].sum()],
        "existing": [summary["existing"].sum()]
    })
    summary_table = pd.concat([summary, totals], ignore_index=True)
    print(summary_table)


    if missing_bc_bce(): # true if missing or checked is False
        asyncio.run(translate_bc_bce(language)) # translate the missing 'bc' and 'bce' entries for span_bce, span_bc and span_ce tags

    # Update 'span_ce', 'span_bce', 'span_bc' and 'float' entries if checked is False


    # Step 8.2: Fix 'span_ce' entries - overwrite if checked is False

    # Step 8.3: Fix 'span_bce' entries

    # Step 8.4: Fix 'span_bc' entries

    # Step 8.5: Fix 'float' entries

    print("\nTranslating ...")
    number_characters = 0      # you can translate up to 500,000 characters per month for free
        # asyncio.run(translate_dictionary(dict_translated, language)) # translate the dictionary
        # print(dict_translated)
        # print("Exporting ...")
        # dict_translated.to_csv(filename, index=False)
    print(f"You translated {number_characters} characters.")
