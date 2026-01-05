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
    # Check execution location, exit if not in /timeline/db
    if os.getcwd()[-12:].replace("\\", "/") != "/timeline/db":
        print("This script must be executed inside the /timeline/db folder.")
        exit()
    if os.path.isfile(filename):
        print("A file with this name already exists.")
        print(f"Importing existing dictionary_{language}.csv file for comparison...")
        dict_translated = pd.read_csv(filename)
        dict_translated.fillna(" ", inplace=True) # fill empty cells with a space
        print(f"The reference dictionary has {len(dict)} entries. The existing dictionary has {len(dict_translated)} entries.")
        # Compare existing: key match the row?
        # Compare existing: notes and text vs english
        # If different, ask user if they want to sync from reference dictionary

        
        # Ensure both DataFrames have the same length
        min_len = min(len(dict), len(dict_translated))
        changed_dictionary = False
        matching_keys = True

        for i in range(min_len):
            row_dict  = dict.iloc[i]
            row_trans = dict_translated.iloc[i]

            # Compare keys
            if row_dict["key"] != row_trans["key"]:
                print(f"Row {i}: Key mismatch -> dict: {row_dict['key']} | dict_translated: {row_trans['key']}")
                matching_keys = False

            notes_dict = dict.iloc[i]["notes"]
            notes_trans = dict_translated.iloc[i]["notes"]

            if notes_dict != notes_trans:
                print(f"\nRow {i}: Notes mismatch")
                print(f"  dict:            {notes_dict}")
                print(f"  dict_translated: {notes_trans}")

                # Ask user if they want to sync
                choice = input("Do you want to sync dict's notes into dict_translated? (y/n): ").strip().lower()
                if choice == "y":
                    dict_translated.at[i, "notes"] = notes_dict
                    print("✅ Synced.")
                    changed_dictionary = True
                else:
                    print("❌ Skipped.")
            
            # Compare text vs english
            text_dict = dict.iloc[i]["text"]
            text_trans = dict_translated.iloc[i]["english"]

            if text_dict != text_trans and dict.iloc[i]["key"] != "daniel2_shift": # exception for this shift value in line 339
                print(f"\nRow {i}: Text mismatch")
                print(f"  dict:            {text_dict}")
                print(f"  dict_translated: {text_trans}")

                # Ask user if they want to sync
                choice = input("Do you want to sync dict's text into dict_translated? (y/n): ").strip().lower()
                if choice == "y":
                    dict_translated.at[i, "english"] = text_dict
                    print("✅ Synced.")
                    changed_dictionary = True
                else:
                    print("❌ Skipped.")

        print("\nComparison completed.")
        if matching_keys:
            print("All keys match between the two dictionaries.")

        # Ask user if they want to save the changes
        if changed_dictionary:
            choice = input("⚠️ Do you want to SAVE your changes? (y/n): ").strip().lower()
            if choice == "y":
                dict_translated.to_csv(filename, index=False)
                print(f"\nAll changes saved to {filename}")
                print("✅ Saved.")
            else:
                print("❌ Skipped.")

        # Are there some entries missing?
        if len(dict) > len(dict_translated):
            print(f"\nThe reference dictionary has {len(dict)} entries, but the existing dictionary has only {len(dict_translated)} entries.")
            print("Some entries are missing in the existing dictionary.")


        user_input = input("A file with this name already exists. Do you want to overwrite it? (yes/no): ")
        # Check user input
        if user_input.lower() == "yes" or user_input.lower() == "":
            print("Proceeding...")
        elif user_input.lower() == "no":
            print("Exiting...")
            exit()
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            exit()
    else:
        print(f"Creating a new dictionary_{language}.csv file.")
        dict_translated = dict[['key', 'text']].copy()   # create a new dictionary, copy columns key and text
        dict_translated['english'] = dict['text'].copy() # add a column 'english' and fill with 'text' from english dictionary
        dict_translated['notes'] = dict['notes'].copy()  # add a column 'notes' and fill with 'notes' from english dictionary

def import_reference():
    global dict
    # print("Import reference english dictionary: ", end="")
    dict = pd.read_csv("./dictionary_reference.csv")
    dict.fillna(" ", inplace=True) # fill empty cells with a space
    # print(f"found {len(dict)} entries.")
    # print(dict)

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
    dict_translated = pd.DataFrame() # columns 'key', 'text' for translated, 'english' for reference, 'notes' to compare, plus 'checked'

    check_existing(language, filename)

    # create the dataframe
    dict_translated = dict[['key', 'text']].copy()   # create a new dictionary, copy columns key and text
    dict_translated['english'] = dict['text'].copy() # add a column 'english' and fill with 'text' from english dictionary
    dict_translated['notes'] = dict['notes'].copy()  # add a column 'notes' and fill with 'notes' from english dictionary
    print("\nTranslating ...")
    number_characters = 0      # you can translate up to 500,000 characters per month for free
    asyncio.run(translate_dictionary(dict_translated, language)) # translate the dictionary
    print(dict_translated)
    print("Exporting ...")
    dict_translated.to_csv(filename, index=False)
    print(f"You translated {number_characters} characters.")
