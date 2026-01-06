import csv

# Reference ISO 639-1 codes (partial example)
iso_map = {
    "en": "English",
    "vi": "Vietnamese",
    "ts": "Tsonga",
    # add more as needed
}

# Compare with supported_languages.csv
with open("../db/supported_languages.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        code = row["key"].strip()
        name = row["language_str"].strip()
        if code in iso_map and iso_map[code] != name:
            print(f"⚠️ Mismatch: key={code}, CSV says '{name}', expected '{iso_map[code]}'")

