# Create a google translated dictionary as starting point for a new language
# It does not work with https://pypi.org/project/googletrans/ 3.0.0 (latest version)
# You need the 3.1.0a0 alpha version from 2020
# pip3 install googletrans==3.1.0a0
# https://pypi.org/project/googletrans/3.1.0a0/ 

import os, sys
import pandas as pd
from googletrans import Translator

def check_existing(language, filename):
    # Check execution location, exit if not in /timeline/db
    if os.getcwd()[-17:].replace("\\", "/") != "/timeline/db/test":
        print("This script must be executed inside the /timeline/db/test folder.")
        exit()
    if os.path.isfile(filename):
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
        print(f"Creating a new mini_{language}.tsv file.")

def import_english():
    global dict
    print("Import english mini file: ", end="")
    dict = pd.read_csv("./mini_en.tsv", sep="\t")
    dict = key_dict.fillna(" ")
    print(f"found {len(dict)} entries.")
    print(dict)

if __name__ == "__main__":
    dict = pd.DataFrame() # will contain the english dictionary with 'key' and 'text' column, plus 'alternative' and 'notes' (not used)
    if len(sys.argv) < 2:
        print("You did not provide a language as argument. Put it as a parameter after the program name.")
        exit()
    language = sys.argv[1]
    filename = "./mini_" + language + ".tsv"
    print(f"You want to translate to {language}.")
    check_existing(language, filename)
    import_english()
    # create the dataframe
    dict_translated = dict[['key', 'text']].copy()   # create a new dictionary, copy columns key and text
    dict_translated['english'] = dict['text'].copy() # add a column 'english' and fill with 'text' from english dictionary
    print("\nTranslating ...")
    translator = Translator()
    for index, row in dict_translated.iterrows(): # with 3 columns 'key' 'text' and 'english'
        english_text = row.english
        if not english_text == " ": # it only applies to row with empty strings - causes translation error
            dict_translated.at[index, 'text'] = translator.translate(english_text, src='en', dest=language).text
            print('.', end='')
        if (index + 1) % 40 == 0:
            print(f" {index}")

    print(dict_translated)
    print("Exporting ...")
    dict_translated.to_csv(filename, index=False, sep="\t")
