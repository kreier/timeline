# Automatically update all dictionaries to align with the reference dictionary

import pandas as pd
import subprocess
import sys

# Load supported languages
df = pd.read_csv("supported_languages.csv")

# Filter only languages where dict == True
langs = df.loc[df["dict"] == True, "key"].tolist()


# Run auto-translate.py for each supported language
for lang in langs:
    print(f"Running auto-translate.py with parameter: {lang}")
    result = subprocess.run(
        [sys.executable, "auto-translate.py", lang]
    )

    if result.returncode != 0:
        print(f"ERROR: Translation failed for language {lang}")
        sys.exit(result.returncode)
