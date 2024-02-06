# Create a google translated dictionary as starting point for a new language

import os, sys
import pandas as pd
from googletrans import Translator

def check_existing(language, filename):
    # Check execution location, exit if not in /timeline/db
    if os.getcwd()[-12:].replace("\\", "/") != "/timeline/db":
        print("This script must be executed inside the /timeline/db folder.")
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
        print(f"Creating a new dictionary_{language}.tsv file.")

def import_english():
    global dict
    print("Import english dictionary: ", end="")
    dict = pd.read_csv("./dictionary_en.tsv", sep="\t")
    print(f"found {len(dict)} entries.")
    print(dict)

def second_func():
    print("Import english dictionary")
    print("Check if target language already exists")
    print("start a dialog: Do you want to overwrite?")
    print("Auto translation done. Translated x key phrases.")

if __name__ == "__main__":
    dict = pd.DataFrame()
    if len(sys.argv) < 2:
        print("You did not provide a language as argument. Put it as a parameter after the program name.")
        exit()
    language = sys.argv[1]
    filename = "./dictionary_" + language + ".tsv"
    print(f"You want to translate to {language}.")
    check_existing(language, filename)
    import_english()
    # create the dataframe
    dict_translated = dict[['key', 'text']].copy()
    dict_translated['english'] = dict['text'].copy()
    print("\nTranslating ...")
    translator = Translator()
    for index, row in dict_translated.iterrows():
        # dict_translated.at[index, 'text'] = "new"
        english_text = row.english
        if not english_text == " ": # it only applies to row 9 where in english is an empty string (unline Vietnamese or Russian)
            dict_translated.at[index, 'text'] = translator.translate(row.english, src='en', dest=language).text
            print('.', end='')
        if (index + 1) % 40 == 0:
            print(f" {index}")

    print(dict_translated)
    print("Exporting ...")
    dict_translated.to_csv(filename, index=False, sep="\t")