# Created with ChatGPT
# Prompt:

# Show current shift values in dictionaries:
# Please write a python script show_values.py that looks first 
# at ../../../db/supported_languages.csv and for the language codes 
# in the 'key' column that have a 'True' in the 'dict' column. 
# For these language codes, use them to check the 
# individual ../../../db/dictionary_XX.csv files where XX is replaced 
# with the language code. In a row with the 'key' value 'daniel2_shift' 
# find the value in the 'text' column and print out the language and the value.

#!/usr/bin/env python3
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUPPORTED_LANG_FILE = os.path.normpath(
    os.path.join(BASE_DIR, "../../../db/supported_languages.csv")
)

DICT_DIR = os.path.normpath(
    os.path.join(BASE_DIR, "../../../db")
)

TARGET_KEY = "daniel2_shift"


def read_supported_languages():
    langs = []
    with open(SUPPORTED_LANG_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("dict", "").strip().lower() == "true":
                langs.append(row.get("key", "").strip())
    return langs


def find_shift_value(lang_code):
    filename = f"dictionary_{lang_code}.csv"
    path = os.path.join(DICT_DIR, filename)

    if not os.path.exists(path):
        return None

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("key", "").strip() == TARGET_KEY:
                return row.get("text", "").strip()
    return None


def main():
    langs = read_supported_languages()

    for lang in langs:
        value = find_shift_value(lang)
        if value is None:
            print(f"{lang}: <not found>")
        else:
            print(f"{lang}: {value}")


if __name__ == "__main__":
    main()
