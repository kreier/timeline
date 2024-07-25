# replace numerals in a given dictionary with the required ones

import os, sys
import pandas as pd

languages_special_numerals = {'ar': 'arabic_numerals',
                            'fa': 'farsi_numerals',
                            'si': 'sinhala_numerals',
                            'km': 'khmer_numerals',
                            'kmar': 'km_to_ar'}
arabic_numerals = {
    '0': '٠',  '1': '١',  '2': '٢',  '3': '٣',  '4': '٤',
    '5': '٥',  '6': '٦',  '7': '٧',  '8': '٨',  '9': '٩'}
farsi_numerals = {
    '0': '۰',  '1': '۱',  '2': '۲',  '3': '۳',  '4': '۴',
    '5': '۵',  '6': '۶',  '7': '۷',  '8': '۸',  '9': '۹'}
sinhala_numerals = {
    '0': '෦',  '1': '෧',  '2': '෨',  '3': '෩',  '4': '෪',
    '5': '෫',  '6': '෬',  '7': '෭',  '8': '෮',  '9': '෯'}
khmer_numerals = {
    '0': '០',  '1': '១',  '2': '២',  '3': '៣',  '4': '៤',
    '5': '៥',  '6': '៦',  '7': '៧',  '8': '៨',  '9': '៩'}
km_to_ar = {
    '០': '0',  '១': '1',  '២': '2',  '៣': '3',  '៤': '4',
    '៥': '5',  '៦': '6',  '៧': '7',  '៨': '8',  '៩': '9'}

def replace(file, numerals):
    dictionary = pd.read_csv(file, encoding='utf8')
    print(f"Imported dictionary with {len(dictionary)} entries")
    new_numerals = globals()[numerals].copy()
    translation_table = str.maketrans(new_numerals)
    # test = "ឆ្នាំ​១៩១៤​ដល់​ឆ្នាំ​១៩១៨ គ.ស."
    # print(test.translate(translation_table))
    counter_found = 0
    for index, row in dictionary.iterrows():
        contains_numerals = False
        for key, value in new_numerals.items():
            if key in str(row.text):
                contains_numerals = True
        if contains_numerals:
            new_string = str(row.text)
            for key, value in new_numerals.items():
                new_string.replace(key, value)
            # new_string.translate(translation_table)
            print(index+1, new_string)
            counter_found += 1
    print(f"Found {counter_found} lines to translate.")
    # print(f"I used the translation table {translation_table}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You did not provide the source file as argument. Put it after this .py file")
        exit()
    source = sys.argv[1]
    target = "kmar"
    filename_source = "../../db/dictionary_" + source + ".csv"
    if target in languages_special_numerals:
        numerals_target = languages_special_numerals[target]
    else:
        numerals_target = "**not supported**"
    print(f"You want to replace the numerals in {filename_source} with {numerals_target} numerals.")
    if os.path.exists(filename_source):
        print("Sourcefile exists.")
        replace(filename_source, numerals_target)
    else:
        print(f"Could not find source file {filename_source}")
