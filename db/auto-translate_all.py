# Automatically update all dictionaries to align with the reference dictionary

import pandas as pd
import subprocess

# Load supported languages
df = pd.read_csv("supported_languages.csv")

# Filter only languages where dict == True
langs = df.loc[df["dict"] == True, "key"].tolist()


# Run auto-translate.py for each supported language
for lang in langs:
    print(f"Running auto-translate.py with parameter: {lang}")
    subprocess.run(["python", "auto-translate.py", lang])
