# Create a Azure translated dictionary as starting point for a new language
# You will need a (free) Azure account to access the API

import os, sys, requests, uuid, json
import pandas as pd

# subscription_key = 'e87e0ed07a914b4c9fe6f1d31c122104'  # this was the 'free' service at hcmc for a year that ended after 1 month
subscription_key = '5c65938c6cc44ca78776725d716c8fe5'  # since the free account could not be activated this became the pay-as-you-go account
region = 'southeastasia'
endpoint = 'https://api.cognitive.microsofttranslator.com/'

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
        print(f"Creating a new mini_{language}.csv file.")

def import_english():
    global dict
    print("Import english mini file: ", end="")
    # dict = pd.read_csv("./mini_en.tsv", sep="\t")
    dict = pd.read_csv("./mini_en.csv")
    dict = dict.fillna(" ")
    print(f"found {len(dict)} entries.")
    print(dict)

if __name__ == "__main__":
    dict = pd.DataFrame() # will contain the english dictionary with 'key' and 'text' column, plus 'alternative' and 'notes' (not used)
    if len(sys.argv) < 2:
        print("You did not provide a language as argument. Put it as a parameter after the program name.")
        exit()
    language = sys.argv[1]
    filename = "./mini_" + language + ".csv"
    print(f"You want to translate to {language}.")
    check_existing(language, filename)
    import_english()
    # create the dataframe
    dict_translated = dict[['key', 'text']].copy()   # create a new dictionary, copy columns key and text
    dict_translated['english'] = dict['text'].copy() # add a column 'english' and fill with 'text' from english dictionary
    print("\nTranslating ...")
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
        english_text = row.english
        number_characters += len(english_text)
        if not english_text == " ": # it only applies to row with empty strings - causes translation error
            body = [ {'Text' : english_text} ]
            request = requests.post(constructed_url, headers=headers, json=body)
            response = request.json()
            # print(response)
            translated_text = response[0]['translations'][0]['text']
            dict_translated.at[index, 'text'] = translated_text
            print(f'{english_text} - {translated_text}')


    print(dict_translated)
    print("Exporting ...")
    dict_translated.to_csv(filename, index=False)
    print(f"You translated {number_characters} characters.")
