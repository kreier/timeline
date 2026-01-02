import csv
import os

# Reference file
languages_file = "languages_website.csv"
# Output markdown file
output_file = "languages_table.md"

rows_out = []

# Read reference file
with open(languages_file, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        lang = row["language"].strip()
        lang_str = row["language_str"].strip()

        # First column: link to timeline_XX.pdf
        lang_link = f"[{lang_str}](https://timeline24.github.io/timeline_{lang}.pdf)"

        # Second column: link to timeline_XX_print.pdf
        print_link = f"[link](https://timeline24.github.io/timeline_{lang}_print.pdf)"

        # Third column: version from dictionary_XX.csv
        dict_file = f"../db/dictionary_{lang}.csv"
        version_text = ""
        last_updated = ""
        if os.path.exists(dict_file):
            with open(dict_file, newline='', encoding="utf-8") as dfile:
                dreader = csv.DictReader(dfile)
                for drow in dreader:
                    if drow["key"].strip() == "version":
                        version_text = drow["text"].strip()
                    if drow["key"].strip() == "pdf_title":
                        last_updated = drow["notes"].strip()

        rows_out.append([lang_link, print_link, version_text, last_updated])

# Build markdown table
with open(output_file, "w", encoding="utf-8") as outmd:
    outmd.write("| language | print | version | last updated |\n")
    outmd.write("|:--------:|:-----:|:-------:|:------------:|\n")
    for r in rows_out:
        outmd.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |\n")

print(f"Markdown table written to {output_file}")
