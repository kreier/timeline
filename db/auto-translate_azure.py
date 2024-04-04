# Create a Azure translated dictionary as starting point for a new language
# You will need a (free) Azure account to access the API

import os, sys, requests, uuid, json
import pandas as pd

# subscription_key = 'e87e0ed07a914b4c9fe6f1d31c122104' # account 2
subscription_key = '5c65938c6cc44ca78776725d716c8fe5' # account 1
region = 'southeastasia'
endpoint = 'https://api.cognitive.microsofttranslator.com/'

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
        print(f"Creating a new dictionary_{language}.csv file.")

def import_reference():
    global dict
    print("Import reference english dictionary: ", end="")
    # dict = pd.read_csv("./dictionary_en.tsv", sep="\t")
    dict = pd.read_csv("./dictionary_reference.csv")
    print(f"found {len(dict)} entries.")
    print(dict)

if __name__ == "__main__":
    dict = pd.DataFrame() # will contain the english dictionary with 'key' and 'text' column, plus 'alternative' and 'notes' (not used)
    if len(sys.argv) < 2:
        print("You did not provide a language as argument. Put it as a parameter after the program name.")
        exit()
    language = sys.argv[1]
    filename = "./dictionary_" + language + ".csv"
    print(f"You want to translate to {language}.")
    check_existing(language, filename)
    import_reference()
    # create the dataframe
    dict_translated = dict[['key', 'text', 'notes']].copy()   # create a new dictionary, copy columns key and text
    dict_translated['english'] = dict['text'].copy() # add a column 'english' and fill with 'text' from english dictionary
    print("\nTranslating ...")
    # translator = Translator()
    number_characters = 0      # you can translate up to 2,000,000 characters per month for free in S0 tier for 12 months

    # Setup Azure AI Translator https://azure.microsoft.com/en-us/products/ai-services/ai-translator
    path = '/translate?api-version=3.0'
    params = '&from=en&to=' + language
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    for index, row in dict_translated.iterrows(): # with 3 columns 'key' 'text' and 'english'
        # dict_translated.at[index, 'text'] = "new"
        english_text = row.english
        number_characters += len(english_text)
        if not english_text == " ": # applies to fields with an empty string
            body = [ {'Text' : english_text} ]
            request = requests.post(constructed_url, headers=headers, json=body)
            response = request.json()
            # print(response)
            translated_text = response[0]['translations'][0]['text']
            dict_translated.at[index, 'text'] = translated_text
            print(f'{english_text} - {translated_text}')

            # it was just this one line with Google Translate and the googletrans API
            # dict_translated.at[index, 'text'] = translator.translate(english_text, src='en', dest=language).text

            # print('.', end='')
            # print(f'English: {english_text}, Translated: {dict_translated[index]}')
        if (index + 1) % 40 == 0:
            print(f" {index}")

    print(dict_translated)
    print("Exporting ...")
    dict_translated.to_csv(filename, index=False)
    print(f"You translated {number_characters} characters.")
