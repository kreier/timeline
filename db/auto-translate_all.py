# Automatically update all dictionaries to align with the reference dictionary

import subprocess

langs = ["en", "de", "vi", "ru", "pt", "es", "it", "ms", "et", "km", "fr"]

for lang in langs:
    print(f"Running auto-translate.py with parameter: {lang}")
    subprocess.run(["python", "auto-translate.py", lang])
