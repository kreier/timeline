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

# Load supported_languages.csv into a dict {key -> language_str}
language_map = {}
with open(languages_file, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        code = row["key"].strip()
        language_str = row["language_str"].strip()
        language_map[code] = language_str

# Pattern to find all language files
files = actual_dict_files
print(f"\nProcessing {len(files)} language files for statistics...")

def normalize_tag(tag):
    tag = tag.strip().lower()
    if tag in ["a6-a", "a6-b"]:
        return "Appendix A6"
    elif tag in ["timespan", "span_ce", "span_bc", "span_bce"]:
        return "Timespan"
    elif tag in ["scripture", "float", "deprecated"]:
        return "Other"
    elif tag in ["text", "bible", "b9", "wiki"]:
        return tag.capitalize() if tag != "b9" else "B9"
    else:
        return "Unknown"




# Output file
output_file = "../history/statistics.csv"

summary = []

for f in files:
    code = os.path.basename(f)[len("dictionary_"):-len(".csv")]
    with open(f, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        length = len(rows)

        checked_true = None
        percentage = ""
        tag_counts = {}

        if "checked" in reader.fieldnames:
            checked_rows = [row for row in rows if row["checked"].strip().upper() == "TRUE"]
            checked_true = len(checked_rows)
            percentage = (checked_true / length * 100) if length > 0 else 0

            # Categorize by normalized tag
            if "tag" in reader.fieldnames:
                for row in checked_rows:
                    tag = normalize_tag(row["tag"])
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Calculate percentages per tag category
        tag_percentages = {}
        if length > 0:  # use total rows as denominator
        # if checked_true and checked_true > 0:
            for tag, count in tag_counts.items():
                tag_percentages[tag] = round(count / length * 100, 2)

        summary.append({
            "language": code,
            "language_str": language_map.get(code, ""),  # add human-readable name
            "length": length,
            "checked_true": checked_true if checked_true is not None else "",
            "percentage_checked_true": percentage if percentage != "" else "",
            "tag_percentages": tag_percentages  # NEW FIELD
        })

summary.sort(
    key=lambda x: (x["percentage_checked_true"] if x["percentage_checked_true"] != "" else -1),
    reverse=True
)

tag_categories = ["Text", "Bible", "B9", "Wiki", "Appendix A6", "Timespan", "Other", "Unknown"]

# Open the file for writing
with open(output_file, "w", newline='', encoding="utf-8") as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames=[
        "language", "language_str", "length", "checked_true", "percentage_checked_true"
    ] + tag_categories)
    writer.writeheader()
    for entry in summary:
        pct = f"{entry['percentage_checked_true']:.2f}%" if entry["percentage_checked_true"] != "" else ""
        row = {
            "language": entry["language"],
            "language_str": entry["language_str"],
            "length": entry["length"],
            "checked_true": entry["checked_true"],
            "percentage_checked_true": pct,
        }
        for cat in tag_categories:
            row[cat] = f"{entry['tag_percentages'].get(cat, 0):.2f}%" if entry["checked_true"] else ""
        writer.writerow(row)


# Print results for languages where "checked" column exists
for entry in summary:
    if entry["checked_true"] != "":
        pct = f"{entry['percentage_checked_true']:.1f}%"
        print(f"{entry['language']} - {entry['language_str']}: length={entry['length']}, "
              f"checked_true={entry['checked_true']}, percentage={pct}")
        if entry["checked_true"] == 0:
            print(f"⚠️ Warning: {entry['language']} has a 'checked' column but no TRUE values")

