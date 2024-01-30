
'''
from googletrans import Translator

# Create a translator object
translator = Translator()

# String to translate
string_to_translate = "Hallo wie geht es dir?"

# Detect the source language
detected_language = translator.detect(string_to_translate).lang
print(detected_language)

# Translate the string to English
translated_string = translator.translate(string_to_translate, src='de', dest='en').text

# Print the translated string
print(translated_string)
'''

import pandas as pd

# Create a sample DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})

# Change the value of the cell at row 1 and column 'B' to 10
df.at[1, 'B'] = 10

# Print the modified DataFrame
print(df)
