# Create a google translated dictionary as starting point for a new language
# Updated to work with with https://pypi.org/project/googletrans/ 4.0.2 (latest version)
# Usage: python auto-translate.py [language_code]
# Update 2026: check the translation, expand if necessary

# dictionary_reference.csv has 'key', 'version', 'english', 'notes', 'tag'                 and               'link' - 2026-06-30
# dictionary_XX.csv        has 'key', 'text',    'english', 'notes', 'tag', 'checked', 'checked_by', 'date', 'link', 'google', 'chatgpt', 'gemini', 'claude', 'deepl'

# Step 1: Compare the number of keys in both dictionaries and report differences
# Step 2: Find keys that are in dict_translated but not in dict
# Step 3: Check if dict_translated has the required columns
# Step 4: Find keys that are in dict but not in dict_translated
# Step 5: Match the order of entries in dict_translated to match dict
# Step 5.1: align dict_translated to dict's key order
# Step 5.2: find extra rows (keys not in dict)
# Step 5.3: mark them as deprecated
# Step 5.4: concatenate aligned first, extras at the end
# Step 6: Check entries in the tag column
# Step 6.1 Count missing tag entries
# Step 6.2 Find mismatches between dict and dict_translated
# Step 6.3 Update dict_translated's tag values to match dict, checked to FALSE
# Step 7: Check entries in the checked column
# Step 8: Compare known entries and fix them
# Step 8.1: match all entries with tag 'timespan' and set checked to True
# Step 8.2: Match the version number and date
# Step 8.3: Compare the values in "english" between dict and dict_translated, set checked to FALSE, update english
# Step 9: Find empty entries in 'text' and send them for translation via googletrans (fill_missing_text)
# Step 10: Find empty entries in the 'google' column (tag == 'text') and fill them via googletrans,
#          kept separate from 'text' so the reviewed/final translation isn't overwritten (fill_missing_google)


import random
import os, sys, asyncio
from time import time
import pandas as pd
from googletrans import Translator
import deepl

# Initialize the DeepL client
# Best practice: Store key in environment variable DEEPL_API_KEY
DEEPL_KEY = os.getenv("DEEPL_API_KEY", "your-deepl-api-key-here")
translator = deepl.Translator(DEEPL_KEY)

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
        dict_translated.fillna(" ", inplace=True)     # fill empty cells with a space
        dict_translated.to_csv(filename, index=False) # save back to ensure the file is cleaned and standardized for further processing

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
            if "tag" in extra_entries.columns:
                # Filter out rows where tag == "deprecated"
                filtered_entries = extra_entries[extra_entries["tag"] != "deprecated"]
            else:
                # If no "tag" column, keep everything
                filtered_entries = extra_entries

            # Print only if there are entries left after filtering
            if not filtered_entries.empty:
                print(filtered_entries)
            print(f"Found some {len(extra_entries)} extra entries, {len(filtered_entries)} will "
                  f"be relabeled as deprecated:") # Step 5.3

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
        required_cols = ["key", "text", "english", "notes", "tag", "checked", "checked_by", "date", "link", "google", "chatgpt", "gemini", "claude", "deepl"]
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
            # Create a mask for rows where the tag will change
            tag_changed = merged["tag_dict"].notna() & (merged["tag_dict"] != dict_translated["tag"])
            # Update tags
            dict_translated["tag"] = merged["tag_dict"].fillna(dict_translated["tag"])
            # Reset 'checked' to False where tag was changed
            # dict_translated.loc[tag_changed, "checked"] = False
            # Show only the rows that changed
            changed_rows = dict_translated.loc[tag_changed]
            print("Rows that were updated:")
            print(changed_rows)
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
        # Initially it was nice to be that verbose:
        # print(f"TRUE values: {num_true}")
        # print(f"FALSE values: {num_false}")
        # print(f"Empty values: {num_empty}")
        # print(f"NaN values: {num_nan}")
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
        dict_translated = dict[['key']].copy()              # create a new dictionary, copy columns key and text
        dict_translated['text'] = " "                       # add a column 'text' and fill with empty string
        dict_translated['english'] = dict['english'].copy() # add a column 'english' and fill with 'text' from english dictionary
        dict_translated['notes'] = dict['notes'].copy()     # add a column 'notes' and fill with 'notes' from english dictionary
        dict_translated['tag'] = dict['tag'].copy()         # add a column 'tag' and fill with 'tag' from english dictionary
        dict_translated['checked'] = False                  # add a column 'checked' and fill with False

    # Step 8: Compare known entries and fix them
    # Step 8.1: match all entries with tag 'timespan' and set checked to True
    mask = dict["tag"] == "timespan"                        # find all timespan entries in the reference dictionary
    lookup = dict.loc[mask].set_index("key")["english"]     # create a lookup series with key and text for timespan entries
    # Update dict_translated text for timespan entries
    update_mask = dict_translated["key"].isin(lookup.index)
    dict_translated.loc[update_mask, "text"] = dict_translated.loc[update_mask, "key"].map(lookup)
    dict_translated.loc[update_mask, "checked"] = True
    # Step 8.2: Match the version number and date
    dict_translated.loc[dict_translated['key'] == 'version', 'english'] = \
        dict.loc[dict['key'] == 'version', 'english'].values
    dict_translated.loc[dict_translated['key'] == 'version', 'text'] = \
        dict.loc[dict['key'] == 'version', 'english'].values
    dict_translated.loc[dict_translated['key'] == 'pdf_title', 'notes'] = \
        dict.loc[dict['key'] == 'pdf_title', 'notes'].values

    # Step 8.3: Compare the values in "english" between dict and dict_translated
    # Index both by 'key'
    dict_indexed = dict.set_index("key")
    trans_indexed = dict_translated.set_index("key")
    # Restrict to common keys
    common_keys = dict_indexed.index.intersection(trans_indexed.index)
    # Align both DataFrames to common keys
    dict_common = dict_indexed.loc[common_keys]
    trans_common = trans_indexed.loc[common_keys]
    # Build mismatch mask (skip daniel2_shift)
    mask = (dict_common["english"] != trans_common["english"]) & (common_keys != "daniel2_shift")
    # Keys to update
    keys_to_update = common_keys[mask]
    # Update english values in dict_translated
    dict_translated.loc[dict_translated["key"].isin(keys_to_update), "english"] = dict_common.loc[keys_to_update, "english"].values
    # Set checked = False for mismatches
    dict_translated.loc[dict_translated["key"].isin(keys_to_update), "checked"] = False
    # Print changed rows
    if len(keys_to_update) > 0:
        print(f"Updated {len(keys_to_update)} rows in dict_translated:")
        print(dict_translated[dict_translated["key"].isin(keys_to_update)])

    dict_translated.to_csv(filename, index=False)

    # Step 8.4: Compare the values in "link" between dict and dict_translated - this will be interactive with three windows
    # to see both wikipedia pages (reference and translated) and the dictionary entry, and decide which link to keep
    # Index both by 'key'
    # If there is no link yet, put the one from the referenc dictionary in. If there is a link, keep it. If the link is different, keep the one in dict_translated.
    # dict_indexed = dict.set_index("key")
    # trans_indexed = dict_translated.set_index("key")
    # # Check if key in dict_translated has a link, if not, copy from dict
    # for key in dict_indexed.index:
    #     if key in trans_indexed.index:
    #         if dict_indexed.at[key, "link"] != " ":
    #             print(f"Checking link for key: {key}, found link: {dict_indexed.at[key, 'link']}, existing link: {trans_indexed.at[key, 'link']}")
    #             # check if trans_indexed.at[key, "link"] is empty or different from dict_indexed.at[key, "link"]
    #             if trans_indexed.at[key, "link"] == " " or trans_indexed.at[key, "link"] != dict_indexed.at[key, "link"]:
    #                 print(f"Updating link for key: {key} to {dict_indexed.at[key, 'link']}")
    #                 dict_translated.loc[dict_translated["key"] == key, "link"] = dict_indexed.at[key, "link"]
    #             # trans_indexed.at[key, "link"] = dict_indexed.at[key, "link"]
    # dict_translated.to_csv(filename, index=False)


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

async def translate_with_googletrans(language, target_col, tag_filter=None, respect_checked=True):
    """
    Shared googletrans worker, used by both fill_missing_text() (Step 9,
    the 'text' column) and fill_missing_google() (Step 10, the 'google'
    suggestion column).

    Translates 'english' into `target_col` for rows where:
      - tag matches tag_filter (if given)
      - checked is False (if respect_checked)
      - english is not empty
      - target_col is currently empty
    Does not touch 'checked' - that column tracks review status of 'text',
    not whether a per-engine suggestion column has been filled.

    Returns the number of characters submitted for translation.
    """
    global dict_translated
    number_characters = 0
    if target_col not in dict_translated.columns:
        dict_translated[target_col] = " "

    mask = pd.Series(True, index=dict_translated.index)
    if tag_filter is not None:
        mask &= dict_translated["tag"] == tag_filter
    if respect_checked:
        mask &= ~dict_translated["checked"]
    mask &= dict_translated["english"] != " "
    mask &= dict_translated[target_col].isna() | (dict_translated[target_col].isin([" ", ""]))

    rows_to_translate = dict_translated[mask].index
    if len(rows_to_translate) == 0:
        print(f"No empty '{target_col}' entries to translate.")
        return number_characters

    # Define retry parameters
    MAX_RETRIES = 3

    for index in rows_to_translate:
        english_text = dict_translated.at[index, "english"]
        number_characters += len(str(english_text))
        translated_success = False

        for attempt in range(MAX_RETRIES):
            try:
                # Open a fresh session to clear rate-limited cookies/connection state if retrying
                async with Translator() as translator:
                    result = await translator.translate(english_text, src="en", dest=language)
                    translated_text = result.text.strip() if result and result.text else ""

                    # Check if we got a valid translation that isn't an unchanged echo
                    if translated_text and translated_text.lower() != english_text.strip().lower():
                        dict_translated.at[index, target_col] = result.text
                        print(f"{index}: {english_text} -> {result.text}")
                        translated_success = True
                        break
                    else:
                        print(f"[{index}] Attempt {attempt + 1}: Received unchanged source text. Retrying...")

            except Exception as e:
                print(f"[{index}] Attempt {attempt + 1} Error: {e}")

            # Exponential backoff with jitter: 3s, 9s, 27s
            backoff_delay = (3 ** (attempt + 1)) + random.uniform(0.5, 1.5)
            await asyncio.sleep(backoff_delay)

        if not translated_success:
            print(f"Skipping index {index}: Max retries reached without a valid translation.")

        # Standard non-blocking delay between successful processing steps to prevent rate limits
        await asyncio.sleep(random.uniform(1.0, 1.8))

    return number_characters


def fill_missing_text(language, filename):
    """
    Step 9: fill missing translations in the 'text' column - the main,
    reviewed/final translation - for all unchecked entries, regardless of tag.
    """
    print("\nStep 9: translating missing 'text' entries ...")
    dict_translated.replace("", " ", inplace=True)  # normalize before checking for empties
    number_characters = asyncio.run(
        translate_with_googletrans(language, target_col="text", tag_filter=None, respect_checked=True)
    )
    if number_characters == 0:
        print("No characters to translate.")
    else:
        print(dict_translated)
        print(f"You translated {number_characters} characters.")
        print("Exporting ...")
        dict_translated.to_csv(filename, index=False)


def fill_missing_google(language, filename):
    """
    Step 10: fill missing 'google' suggestions for rows tagged 'text' that
    don't have one yet. Kept separate from 'text' itself, which holds the
    reviewed/final translation (possibly sourced from a different engine
    or a human), so it isn't overwritten.
    """
    print("\nStep 10: filling 'google' suggestions for tag == 'text' ...")
    number_characters = asyncio.run(
        translate_with_googletrans(language, target_col="google", tag_filter="text", respect_checked=False)
    )
    if number_characters == 0:
        print("No characters to translate for the 'google' column.")
    else:
        print(f"You translated {number_characters} characters for the 'google' column.")
        print("Exporting ...")
        dict_translated.to_csv(filename, index=False)

# Stage 10.2 execution function
def run_stage_10_2(df, target_col="deepl", target_lang="VI"):
    """
    Translates rows where tag == 'text' and target_col cell is missing/empty.
    """
    # 1. Map target language codes if necessary (e.g., 'en' -> 'EN-US')
    lang_upper = target_lang.upper()
    if lang_upper == "EN":
        lang_upper = "EN-US"
        
    # 2. Filter rows that need translation
    rows_to_translate = df[
        (df["tag"] == "text") & 
        (df[target_col].isna() | (df[target_col].astype(str).str.strip() == ""))
    ].index

    print(f"Found {len(rows_to_translate)} rows to translate using DeepL.")

    for index in rows_to_translate:
        english_text = str(df.at[index, "english"])
        
        if not english_text.strip():
            continue

        try:
            # 3. Call DeepL API
            result = translator.translate_text(
                english_text,
                source_lang="EN",
                target_lang=lang_upper
            )
            
            translated_text = result.text.strip()
            
            # Verify translation returned something different from the original text
            if translated_text and translated_text.lower() != english_text.strip().lower():
                df.at[index, target_col] = translated_text
                print(f"[{index}] Success: {english_text} -> {translated_text}")
            else:
                print(f"[{index}] Skipped: Output identical to source text.")

        except deepl.QuotaExceededException:
            print("Error: DeepL character quota exceeded for this month.")
            break
        except deepl.DeepLException as e:
            print(f"[{index}] DeepL API Error: {e}")
        except Exception as e:
            print(f"[{index}] Unexpected error: {e}")

    return df

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

    # Step 1 to 8
    check_existing(language, filename)

    # Step 9: fill missing 'text' translations via googletrans
    # fill_missing_text(language, filename)

    # Step 10: fill missing 'google' suggestions via googletrans
    fill_missing_google(language, filename)

    # Stage 10.2: fill the 'deepl' column via DeepL.
    # NOTE: this still needs to be wired up to run_stage_10_2() (the DeepL
    # function defined above) rather than a googletrans call - left as-is
    # for now since it's a separate translation engine, outside the scope
    # of this googletrans clean-up.
    print("\nStage 10.2: filling 'deepl' suggestions for tag == 'text' ...")
    dict_translated = run_stage_10_2(dict_translated, target_col="deepl", target_lang=language)
    dict_translated.to_csv(filename, index=False)
