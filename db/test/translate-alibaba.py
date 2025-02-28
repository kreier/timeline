# Create a translated dictionary for a new language wit alibaba cloud machine translation
# pip install alibabacloud-alimt20181012 https://pypi.org/project/alibabacloud-alimt20181012/
# with 221 languages

import os, sys
import pandas as pd
from aliyunsdkcore.client import AcsClient
from aliyunsdkalimt.request.v20181012 import TranslateRequest
import json

# Your API credentials
access_key_id = 'import_1'
access_key_secret = 'import_2'
# region = 'cn-hangzhou'
# region = 'cn-shanghai'
region = 'ap-southeast-1'

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
    print("Import english mini dictionary file: ", end="")
    dict = pd.read_csv("./mini_en.csv")
    dict = dict.fillna(" ")
    print(f"found {len(dict)} entries.")
    print(dict)

def translate_dictionary():
    global dict_translated
    global number_characters
    for index, row in dict_translated.iterrows(): # with 3 columns 'key' 'text' and 'english'
        english_text = row.english
        number_characters += len(english_text)
        if not english_text == " ": # it only applies to row with empty strings - causes translation error
            result = ts.translate_text(english_text, translator='alibaba', to_language=language)
            dict_translated.at[index, 'text'] = result.text
            # print('.', end='')
        if (index + 1) % 40 == 0:
            print(f" {index}")

if __name__ == "__main__":
    '''
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
    number_characters = 0      # you can translate up to 500,000 characters per month for free        
    # asyncio.run(translate_dictionary())
    translate_dictionary()
    print(dict_translated)
    print("Exporting ...")
    dict_translated.to_csv(filename, index=False)
    print(f"You translated {number_characters} characters.")
    '''

    # # Your English text
    # text = {"Hello, how are you?", "I am fine, thank you.", "What is your name?", "My name is John."}

    # # Translating to Spanish using Alibaba
    # translated_text = ts.bing(text, to_language='es')

    # print(translated_text)

    # import translators as ts

    # # Array of English texts
    # texts = ["Hello, how are you?", "I am fine, thank you.", "What is your name?", "My name is John."]

    # # Translate each text to Spanish using Bing (since the Alibaba API is currently not supported in the translators library)
    # translated_texts = [ts.bing(text, to_language='es') for text in texts]

    # # Print the translated texts
    # for original, translated in zip(texts, translated_texts):
    #     print(f"Original: {original}\nTranslated: {translated}\n")

    # # Test if it works
    # assert translated_texts[0] == "Hola, ¿cómo estás?"
    # assert translated_texts[1] == "Estoy bien, gracias."
    # assert translated_texts[2] == "¿Cuál es tu nombre?"
    # assert translated_texts[3] == "Mi nombre es John."

    # print("All translations are correct!")


    # Create an AcsClient instance
    client = AcsClient(access_key_id, access_key_secret, region)

    # Create a TranslateRequest instance
    request = TranslateRequest.TranslateRequest()

    # Set the request parameters
    request.set_FormatType('text')
    request.set_SourceLanguage('en')
    request.set_TargetLanguage('es')
    request.set_SourceText('Hello, how are you?')
    request.set_Scene('general')

    # Make the request
    response = client.do_action_with_exception(request)
    translated_text = response['Data']['TargetText']

    print(translated_text)
