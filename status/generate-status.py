"""Generate the translation status page for the timeline project.

Reads db/supported_languages.csv (the "dict" column marks a language as
supported) and cross-checks it against the matching db/dictionary_<key>.csv
file for that language. For every language that has both, it computes:

  - completion (% checked == True) for each of the 6 tag categories used
    by the dictionary editor (text, bible, b9, a6, wiki, others)
  - an overall completion percentage across those categories
  - how many rows carry machine-translation text in the google, chatgpt,
    gemini, claude and deepl columns (as a % of all "text" rows)

Two versions of the table are produced:
  - status/index.md   - the GitHub Pages status page. This is real HTML
    embedded in the Markdown, so the percentage cells get an actual
    red -> yellow -> green background gradient. The page also carries a
    <style> block that widens the primer theme's content area to (almost)
    full width and wraps the wide table in an overflow-x container so it
    is readable without scrolling the whole page.
  - status/README.md  - shown on GitHub's own repo page. GitHub strips
    "style" attributes from HTML in rendered Markdown, so instead of a
    background color each cell gets a coloured square as a stand-in.

Only the Python standard library is used (no pandas), since the GitHub
Actions workflow that runs this script does not install it.
"""

import csv
from pathlib import Path

# Always relative to this Python file, not the current working directory.
STATUS_DIR = Path(__file__).resolve().parent
REPO_ROOT = STATUS_DIR.parent
DB_DIR = REPO_ROOT / "db"

SUPPORTED_LANGUAGES_FILE = DB_DIR / "supported_languages.csv"
# NOTE: the actual per-language files in this repo are named
# db/dictionary_<key>.csv (not db/language_<key>.csv - "dictionary_" is
# the prefix used everywhere else in the codebase, e.g. web_editor.py and
# the approve-translation.yml workflow).
DICTIONARY_PREFIX = "dictionary_"

INDEX_FILE = STATUS_DIR / "index.md"
README_FILE = STATUS_DIR / "README.md"

# The 6 tag categories used by db/dictionary_<key>.csv and the
# python/web_editor/web_editor.py editor. Every dictionary row has a
# "tag" that falls into exactly one of these groups.
TAG_GROUPS = {
    "text": ["text"],
    "bible": ["bible"],
    "b9": ["b9"],
    "a6": ["a6-a", "a6-b"],
    "wiki": ["wiki"],
    "others": ["deprecated", "scripture", "span_bc", "span_bce", "span_ce"],
}
TAG_GROUP_LABELS = {
    "text": "Text",
    "bible": "Bible",
    "b9": "B9",
    "a6": "A6",
    "wiki": "Wiki",
    "others": "Others",
}

# Rows with these tags are metadata (e.g. the "version" row) and are
# excluded from every percentage.
IGNORED_TAGS = {"float"}

# The machine-translation columns to report on.
AI_COLUMNS = ["google", "chatgpt", "gemini", "claude", "deepl"]
AI_COLUMN_LABELS = {
    "google": "Google",
    "chatgpt": "ChatGPT",
    "gemini": "Gemini",
    "claude": "Claude",
    "deepl": "DeepL",
}


def read_csv_rows(path):
    """Read a CSV file into a list of dicts, tolerant of a UTF-8 BOM."""
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def is_true(value):
    return str(value).strip().lower() == "true"


def load_supported_languages():
    """Return {key: language_str} for every language marked dict=TRUE."""
    supported = {}
    for row in read_csv_rows(SUPPORTED_LANGUAGES_FILE):
        key = (row.get("key") or "").strip()
        if not key:
            continue
        if is_true(row.get("dict")):
            supported[key] = (row.get("language_str") or key).strip()
    return supported


def find_dictionary_files():
    """Return {key: path} for every db/dictionary_<key>.csv on disk."""
    files = {}
    for path in DB_DIR.glob(f"{DICTIONARY_PREFIX}*.csv"):
        key = path.stem[len(DICTIONARY_PREFIX):]
        files[key] = path
    return files


def check_consistency(supported, files):
    """Compare supported_languages.csv against the files on disk.

    Returns (matched_keys, missing_files, orphaned_files):
      - missing_files: marked supported but no dictionary_<key>.csv exists
      - orphaned_files: a dictionary_<key>.csv exists but isn't marked
        supported (dict=TRUE) in supported_languages.csv
    """
    supported_keys = set(supported)
    file_keys = set(files)

    matched = sorted(supported_keys & file_keys)
    missing_files = sorted(supported_keys - file_keys)
    orphaned_files = sorted(file_keys - supported_keys)

    return matched, missing_files, orphaned_files


def analyze_dictionary(path):
    """Compute tag-group and AI-column completion stats for one file."""

    rows = [
        r
        for r in read_csv_rows(path)
        if (r.get("tag") or "").strip().lower() not in IGNORED_TAGS
    ]

    group_stats = {}
    for group, tags in TAG_GROUPS.items():
        group_rows = [
            r
            for r in rows
            if (r.get("tag") or "").strip().lower() in tags
        ]
        total = len(group_rows)
        checked = sum(
            1 for r in group_rows if is_true(r.get("checked"))
        )
        pct = round(100 * checked / total, 1) if total else None
        group_stats[group] = {
            "checked": checked,
            "total": total,
            "pct": pct,
        }

    overall_total = sum(g["total"] for g in group_stats.values())
    overall_checked = sum(g["checked"] for g in group_stats.values())
    overall_pct = (
        round(100 * overall_checked / overall_total, 1)
        if overall_total
        else None
    )

    # Machine translations are currently provided only for "text" entries.
    # Therefore, use the number of text entries as the reference/denominator
    # for all AI translation percentages.
    text_rows = [
        r
        for r in rows
        if (r.get("tag") or "").strip().lower() == "text"
    ]
    total_text_rows = len(text_rows)

    ai_stats = {}
    for col in AI_COLUMNS:
        filled = sum(
            1 for r in text_rows if (r.get(col) or "").strip()
        )
        pct = (
            round(100 * filled / total_text_rows, 1)
            if total_text_rows
            else None
        )
        ai_stats[col] = {
            "filled": filled,
            "total": total_text_rows,
            "pct": pct,
        }

    return {
        "groups": group_stats,
        "overall_pct": overall_pct,
        "overall_checked": overall_checked,
        "overall_total": overall_total,
        "ai": ai_stats,
    }


def color_for_percent(pct):
    """Interpolate red (0%) -> yellow (50%) -> green (100%) as a hex color."""
    if pct is None:
        return "#e0e0e0"  # grey for "no data"
    pct = max(0.0, min(100.0, pct))

    red = (220, 53, 69)
    yellow = (255, 193, 7)
    green = (40, 167, 69)

    if pct <= 50:
        t = pct / 50
        start, end = red, yellow
    else:
        t = (pct - 50) / 50
        start, end = yellow, green

    rgb = tuple(
        round(start[i] + (end[i] - start[i]) * t)
        for i in range(3)
    )
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def format_cell_html(pct):
    """A percentage cell with a real colored background (for index.md)."""
    if pct is None:
        return '<td style="background-color:#e0e0e0; text-align:center;">-</td>'
    color = color_for_percent(pct)
    return (
        f'<td style="background-color:{color}; '
        f'text-align:center;">{pct:.1f}%</td>'
    )


def format_cell_readme(pct):
    """A percentage cell with a coloured square stand-in (for README.md)."""
    if pct is None:
        return "| - "
    if pct >= 90:
        square = "🟩"
    elif pct >= 60:
        square = "🟨"
    elif pct >= 30:
        square = "🟧"
    else:
        square = "🟥"
    return f"| {square} {pct:.1f}% "


def build_table_headers():
    group_headers = [TAG_GROUP_LABELS[g] for g in TAG_GROUPS]
    ai_headers = [AI_COLUMN_LABELS[c] for c in AI_COLUMNS]
    return ["Language"] + group_headers + ["Overall"] + ai_headers


def build_html_table(matched, supported, results):
    headers = build_table_headers()
    header_html = "".join(f"<th>{h}</th>" for h in headers)

    rows_html = []

    for key in matched:
        stats = results[key]
        cells = [f"<td>{supported[key]} ({key})</td>"]

        for group in TAG_GROUPS:
            cells.append(
                format_cell_html(stats["groups"][group]["pct"])
            )

        cells.append(format_cell_html(stats["overall_pct"]))

        for col in AI_COLUMNS:
            cells.append(format_cell_html(stats["ai"][col]["pct"]))

        rows_html.append(f"<tr>{''.join(cells)}</tr>")

    table = (
        '<div class="status-table-wrap">\n'
        '<table>\n<thead><tr>'
        + header_html
        + '</tr></thead>\n<tbody>\n'
        + "\n".join(rows_html)
        + "\n</tbody>\n</table>\n"
        '</div>'
    )

    return table


def build_markdown_table(matched, supported, results):
    headers = build_table_headers()

    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "|" + "|".join(["---"] * len(headers)) + "|"

    lines = [header_row, separator_row]

    for key in matched:
        stats = results[key]
        line = f"| {supported[key]} ({key}) "

        for group in TAG_GROUPS:
            line += format_cell_readme(
                stats["groups"][group]["pct"]
            )

        line += format_cell_readme(stats["overall_pct"])

        for col in AI_COLUMNS:
            line += format_cell_readme(stats["ai"][col]["pct"])

        line += "|"
        lines.append(line)

    return "\n".join(lines)


def build_consistency_section(missing_files, orphaned_files):
    if not missing_files and not orphaned_files:
        return ""

    lines = ["", "### ⚠️ Inconsistencies found", ""]

    if missing_files:
        lines.append(
            "Marked `dict=TRUE` in `supported_languages.csv` but no matching "
            f"`db/{DICTIONARY_PREFIX}<key>.csv` file exists:"
        )

        for key in missing_files:
            lines.append(f"- `{key}`")

        lines.append("")

    if orphaned_files:
        lines.append(
            f"A `db/{DICTIONARY_PREFIX}<key>.csv` file exists but the language "
            "isn't marked `dict=TRUE` in `supported_languages.csv`:"
        )

        for key in orphaned_files:
            lines.append(f"- `{key}`")

        lines.append("")

    return "\n".join(lines)


def generate_content():
    """
    Generate the actual status information.

    Returns (html_content, markdown_content) - the HTML version (with real
    colored backgrounds) for index.md, and a Markdown/emoji version for
    README.md, since GitHub strips inline styles from README rendering.
    """
    supported = load_supported_languages()
    files = find_dictionary_files()

    matched, missing_files, orphaned_files = check_consistency(
        supported,
        files,
    )

    results = {
        key: analyze_dictionary(files[key])
        for key in matched
    }

    consistency_section = build_consistency_section(
        missing_files,
        orphaned_files,
    )

    intro = (
        f"Tracking {len(matched)} supported language"
        f"{'s' if len(matched) != 1 else ''} against their "
        f"`db/{DICTIONARY_PREFIX}<key>.csv` files.\n"
        "For each of the 6 tag categories (text, bible, B9, A6, wiki, "
        "others) the percentage shows how many entries are marked "
        "`checked = TRUE`. "
        "The last 5 columns show the percentage of text entries that "
        "already carry machine-translated text from that service."
    )

    html_table = build_html_table(
        matched,
        supported,
        results,
    )

    md_table = build_markdown_table(
        matched,
        supported,
        results,
    )

    html_content = f"""<style>
/* Widen the GitHub Pages (primer theme) content area so the wide
   status table is readable without scrolling the whole page. */
@media (min-width: 768px) {{
  .container-lg {{
    max-width: 96vw !important;
    width: 96vw !important;
  }}
  .markdown-body {{
    max-width: none !important;
  }}
}}
.status-table-wrap {{
  overflow-x: auto;
}}
.status-table-wrap table {{
  border-collapse: collapse;
  white-space: nowrap;
  margin: 0;
}}
.status-table-wrap th,
.status-table-wrap td {{
  font-size: 0.9rem;
}}
</style>

# Timeline status

This page is automatically generated.

{intro}
{consistency_section}

{html_table}
"""

    md_content = f"""# Timeline status

This page is automatically generated.

{intro}
{consistency_section}

{md_table}
"""

    return html_content, md_content


def generate_index(content):
    """Generate the Jekyll page (allows real HTML/CSS, e.g. colored cells)."""

    text = f"""---
layout: default
title: Timeline status
---

{content}
"""

    INDEX_FILE.write_text(text, encoding="utf-8")


def generate_readme(content):
    """Generate the GitHub README (GitHub strips inline "style" attributes,
    so this version uses colored-square emoji instead of backgrounds)."""

    text = f"""{content}
"""

    README_FILE.write_text(text, encoding="utf-8")


def main():
    html_content, md_content = generate_content()

    generate_index(html_content)
    generate_readme(md_content)

    print(f"Generated {INDEX_FILE}")
    print(f"Generated {README_FILE}")


if __name__ == "__main__":
    main()



# Create status/index.md
# Create status/timeline24.md
# Create status/timeline25.md
