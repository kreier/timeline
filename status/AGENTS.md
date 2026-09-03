# Status Folder - LLM Agent Guide

## Purpose

This folder generates translation status reports for the timeline project. The script `generate-status.py` reads dictionary files and produces two output files:

- `index.md` - GitHub Pages version with HTML/CSS colored cells
- `README.md` - GitHub repo version with emoji-colored squares

## Quick Start

```bash
python status/generate-status.py
```

No external dependencies required - uses only Python standard library.

## Data Sources

| File | Location | Purpose |
|------|----------|---------|
| `supported_languages.csv` | `db/` | Languages marked `dict=TRUE` |
| `dictionary_<key>.csv` | `db/` | Translation entries per language |

## Tag Categories

Every dictionary row has a `tag` that falls into one of these groups:

| Category | Tag Values | Description |
|----------|------------|-------------|
| **text** | `text` | Main UI strings (titles, labels, events) |
| **bible** | `bible` | Biblical names (Adam, Moses, etc.) |
| **b9** | `b9` | Daniel 2 appendix entries |
| **a6** | `a6-a`, `a6-b` | Kings of Israel (northern) and Judah (southern) |
| **wiki** | `wiki` | Wikipedia-sourced entries |
| **others** | `deprecated`, `scripture`, `span_bc`, `span_bce`, `span_ce` | Miscellaneous |

Rows with tag `float` (like the version row) are excluded from percentages.

**Ignored keys:**
- `age_kings` - Intentionally empty in most languages (conditional label: "years" vs "year" depending on the numeral)

## CSV Schema (dictionary_*.csv)

```csv
key,text,english,notes,tag,checked,checked_by,date,link,google,chatgpt,gemini,claude,deepl
```

| Column | Description |
|--------|-------------|
| `key` | Unique identifier (e.g., `Deluge`, `Adam`, `BCE`) |
| `text` | Localized string for this language |
| `english` | Reference English string |
| `notes` | Optional notes |
| `tag` | Category tag (see above) |
| `checked` | `TRUE` if translation is reviewed/verified |
| `checked_by` | Name of reviewer (e.g., `Matthias`, `Nam`) |
| `date` | Review date in `YYYY-MM-DD` format |
| `link` | Optional reference link |
| `google` | Google Translate output |
| `chatgpt` | ChatGPT translation |
| `gemini` | Google Gemini translation |
| `claude` | Claude translation |
| `deepl` | DeepL translation |

## Output Sections

The generated reports contain:

1. **Inconsistencies** - Languages marked `dict=TRUE` but missing dictionary file (or vice versa)
2. **Translation Status Table** - 6 tag categories + overall completion percentage
3. **AI Translation Coverage** - Percentage of text entries with machine translations
4. **Translation Reviewers** - Attribution statistics for `checked_by` entries

## Making Changes

### Adding a new tag category
1. Add the tag to `TAG_GROUPS` dictionary
2. Add a label to `TAG_GROUP_LABELS`
3. The table columns update automatically

### Adding a new AI translation column
1. Add column name to `AI_COLUMNS` list
2. Add display label to `AI_COLUMN_LABELS`

### Modifying output format
- HTML version: Edit `format_cell_html()` and `build_html_table()`
- Markdown version: Edit `format_cell_readme()` and `build_markdown_table()`

## Key Functions

| Function | Purpose |
|----------|---------|
| `load_supported_languages()` | Parse `supported_languages.csv` for `dict=TRUE` entries |
| `find_dictionary_files()` | Discover all `dictionary_*.csv` files |
| `analyze_dictionary(path)` | Compute tag-group and AI-column stats for one file |
| `analyze_contributions(matched, files)` | Aggregate `checked_by` statistics across all files |
| `generate_content()` | Main orchestrator returning (html, markdown) content |
| `generate_index(content)` | Write `index.md` with Jekyll frontmatter |
| `generate_readme(content)` | Write `README.md` for GitHub display |

## Notes for LLM Agents

- The script must remain dependency-free (runs in GitHub Actions without pip install)
- GitHub strips `style` attributes from README.md, so use emoji squares there
- index.md supports full HTML/CSS for colored backgrounds
- The `reference` dictionary file exists but is not marked `dict=TRUE` (expected inconsistency)
- Most `checked_by` entries are `Matthias` (project owner); `Nam` is the only other reviewer (6 entries in Vietnamese)
