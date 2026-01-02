import csv
import os
import glob

# Paths
languages_file = "../db/supported_languages.csv"
dictionary_pattern = "../db/dictionary_*.csv"

# Read supported languages
supported = {}
with open(languages_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        code = row["key"].strip()
        has_dict = row["dict"].strip().upper() == "TRUE"
        supported[code] = has_dict

# Collect actual dictionary files
actual_dict_files = glob.glob(dictionary_pattern)
actual_codes = {os.path.basename(f)[len("dictionary_"):-len(".csv")] for f in actual_dict_files}

# Check consistency
missing_files = [code for code, has_dict in supported.items() if has_dict and code not in actual_codes]
extra_files = [code for code in actual_codes if code not in supported or not supported[code]]

print(f"Total supported languages: {len(supported)}")
print(f"Languages with dictionary (expected): {sum(supported.values())}")
print(f"Dictionary files found: {len(actual_codes)}")

if missing_files:
    print("❌ Missing dictionary files for:", ", ".join(missing_files))
else:
    print("✅ No missing dictionary files")

if extra_files:
    print("⚠️ Extra dictionary files not listed in supported_languages.csv:", ", ".join(extra_files))
else:
    print("✅ No extra dictionary files")


# Part II ********************************************************************************************

# Pattern to find all language files
files = actual_dict_files

print(f"\nProcessing {len(files)} language files for statistics...")

# Output file
output_file = "../db/statistics.csv"

summary = []

for f in files:
    code = os.path.basename(f)[len("dictionary_"):-len(".csv")]
    with open(f, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        length = len(rows)

        checked_true = None
        percentage = ""
        if "checked" in reader.fieldnames:
            checked_true = sum(1 for row in rows if row["checked"].strip().upper() == "TRUE")
            percentage = (checked_true / length * 100) if length > 0 else 0

        summary.append({
            "language": code,
            "length": length,
            "checked_true": checked_true if checked_true is not None else "",
            "percentage_checked_true": percentage if percentage != "" else ""
        })

# Sort by percentage (descending), keeping entries without percentage at the end
summary.sort(key=lambda x: (x["percentage_checked_true"] if x["percentage_checked_true"] != "" else -1), reverse=True)

# Write summary CSV
with open(output_file, "w", newline='', encoding="utf-8") as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames=["language", "length", "checked_true", "percentage_checked_true"])
    writer.writeheader()
    for entry in summary:
        # Format percentage nicely for CSV
        pct = f"{entry['percentage_checked_true']:.2f}%" if entry["percentage_checked_true"] != "" else ""
        writer.writerow({
            "language": entry["language"],
            "length": entry["length"],
            "checked_true": entry["checked_true"],
            "percentage_checked_true": pct
        })

# Print results for languages where "checked" column exists
for entry in summary:
    if entry["checked_true"] != "":
        pct = f"{entry['percentage_checked_true']:.2f}%"
        print(f"{entry['language']}: length={entry['length']}, checked_true={entry['checked_true']}, percentage={pct}")
        if entry["checked_true"] == 0:
            print(f"⚠️ Warning: {entry['language']} has a 'checked' column but no TRUE values")

