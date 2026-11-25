#!/usr/bin/env python3
"""
Fill the 'claude' translation column in db/dictionary_*.csv using Claude Sonnet 4.6
(non-thinking) via `agy -p`, with compact biblical/historical context and
persistent stopping-point documentation in db/claude_translation_status.md.
"""

import glob
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
import pandas as pd

sys.stdout.reconfigure(line_buffering=True)

DB_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_PATH = os.path.join(DB_DIR, "claude_translation_status.md")
MODEL_NAME = "claude-sonnet-4-6"
BATCH_SIZE = 100
EXCLUDED_TAGS = {"float", "timespan", "deprecated"}

LANG_NAMES = {
    "ar": "Arabic",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "ceb": "Cebuano",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fa": "Persian",
    "fi": "Finnish",
    "fj": "Fijian",
    "fr": "French",
    "ha": "Hausa",
    "he": "Hebrew",
    "hi": "Hindi",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "ig": "Igbo",
    "ilo": "Iloko",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "kg": "Kikongo",
    "km": "Khmer",
    "kman": "Northern Khmer",
    "kn": "Kannada",
    "kne": "Kankanaey",
    "ko": "Korean",
    "lo": "Lao",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "my": "Burmese",
    "nl": "Dutch",
    "no": "Norwegian",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "si": "Sinhala",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "yue": "Cantonese",
    "zh": "Simplified Chinese",
}


class TokenExhaustedError(Exception):
    """Raised when agy reports token/quota exhaustion or unrecoverable API failure."""


def call_claude_agy(prompt, timeout_sec=180):
    """Invoke `agy` non-interactively with Claude Sonnet 4.6 and return (text, usage)."""
    cmd = [
        "agy",
        "--model", MODEL_NAME,
        "--disable-slash-commands",
        "--output-format", "json",
        f"-p={prompt}",
    ]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()

    # agy --output-format json prints a single JSON object (sometimes preceded by stderr/spinner)
    data = None
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                data = json.loads(line)
                break
            except json.JSONDecodeError:
                pass

    if data is None:
        msg = stderr or stdout or f"exit code {proc.returncode}"
        raise RuntimeError(f"Unparseable agy output: {msg[:300]}")

    status = data.get("status", "")
    usage = data.get("usage", {})
    if status != "SUCCESS" or proc.returncode != 0:
        err = data.get("error") or stderr or stdout or f"status={status}"
        err_lower = str(err).lower()
        if any(k in err_lower for k in ("quota", "exhaust", "limit", "credit", "billing", "insufficient", "429", "rate")):
            raise TokenExhaustedError(str(err)[:300])
        raise RuntimeError(str(err)[:300])

    return data.get("response", ""), usage


def format_item(i, row):
    """Format a single row with compact tag/note context to aid translation."""
    tag = str(row["tag"]).strip() if pd.notna(row["tag"]) else ""
    note = str(row["notes"]).strip() if pd.notna(row["notes"]) else ""
    eng = str(row["english"]).strip()
    # Keep note compact to save tokens
    if note and len(note) <= 60:
        ctx = f"[{tag}|{note}]" if tag else f"[{note}]"
    elif tag:
        ctx = f"[{tag}]"
    else:
        ctx = "[text]"
    return f"{i}. {ctx} {eng}"


def parse_numbered_response(resp_text, count):
    """Parse `N. translation` lines and strip any echoed bracketed context."""
    parsed = {}
    for ln in resp_text.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        m = re.match(r"^(\d+)\.\s*(.*)$", ln)
        if m:
            idx = int(m.group(1))
            val = m.group(2).strip()
            # Strip accidentally echoed [tag] or [tag|note] prefix
            val = re.sub(r"^\[[^\]]+\]\s*", "", val).strip()
            parsed[idx] = val
    if len(parsed) == count and set(parsed.keys()) == set(range(1, count + 1)):
        return [parsed[i] for i in range(1, count + 1)]
    return None


def translate_batch(rows, target_lang, stats, max_retries=2):
    """Translate a list of DataFrame row dicts using Claude Sonnet 4.6."""
    if not rows:
        return []

    numbered = [format_item(i + 1, r) for i, r in enumerate(rows)]
    prompt = (
        f"Do not use any tools. Translate these {len(rows)} items from a Biblical & World History Timeline "
        f"(New World Translation terminology, e.g. B.C.E./C.E., established Bible names) into {target_lang}.\n"
        f"Context tags before each item: [bible]=Bible character/place/term, [A6-A]/[A6-B]=kings/prophets of Judah & Israel, "
        f"[B9]=Biblical calendar/era, [wiki]=world history, [text]=timeline caption.\n"
        f"Translate ONLY the text after the bracketed `[...]` tag. "
        f"Return EXACTLY {len(rows)} lines formatted as `N. translation` (no `[...]` tags, no notes, no markdown, no extra text).\n\n"
        + "\n".join(numbered)
    )

    for attempt in range(max_retries):
        try:
            resp_text, usage = call_claude_agy(prompt)
            for k in ("input_tokens", "output_tokens", "thinking_tokens", "cache_read_tokens", "total_tokens"):
                stats[k] += int(usage.get(k, 0))
            stats["calls"] += 1

            parsed = parse_numbered_response(resp_text, len(rows))
            if parsed is not None:
                return parsed
            print(f"      [Parse retry {attempt + 1}] expected {len(rows)} lines, got mismatch.", flush=True)
        except TokenExhaustedError:
            raise
        except Exception as e:
            print(f"      [Retry {attempt + 1}] {str(e)[:120]}", flush=True)
            time.sleep(4 * (attempt + 1))

    if len(rows) > 1:
        print(f"      Splitting batch of {len(rows)} into halves...", flush=True)
        mid = len(rows) // 2
        return (
            translate_batch(rows[:mid], target_lang, stats, max_retries)
            + translate_batch(rows[mid:], target_lang, stats, max_retries)
        )
    raise RuntimeError(f"Failed to translate single item: {rows[0].get('key')}")


def write_status_doc(file_progress, stats, stop_info=None):
    """Write current progress and any stopping point to db/claude_translation_status.md."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Claude Sonnet 4.6 Translation Status (`claude` column)",
        "",
        f"- **Updated:** {now}",
        f"- **Model:** `{MODEL_NAME}` (non-thinking, `thinking_tokens` observed: {stats['thinking_tokens']})",
        f"- **API Calls:** {stats['calls']}",
        f"- **Items Translated This Run:** {stats['translated']}",
        f"- **Token Usage This Run:** input={stats['input_tokens']:,}, output={stats['output_tokens']:,}, cache_read={stats['cache_read_tokens']:,}, thinking={stats['thinking_tokens']:,}, total={stats['total_tokens']:,}",
        "",
    ]

    if stop_info:
        lines.extend([
            "## Stopping Point (Early Stop)",
            "",
            f"- **Stopped at file:** `{stop_info['file']}`",
            f"- **Batch:** {stop_info['batch']} / {stop_info['total_batches']}",
            f"- **First untranslated key in batch:** `{stop_info['first_key']}`",
            f"- **Reason:** `{stop_info['reason']}`",
            "- **Resume command:** `.venv/bin/python3 db/fill_claude.py` (automatically skips already-filled `claude` cells)",
            "",
        ])
    else:
        lines.extend([
            "## Status",
            "",
            "Run completed without token exhaustion.",
            "",
        ])

    lines.extend([
        "## Per-File Progress",
        "",
        "| File | Language | Filled / Translatable | Remaining |",
        "|------|----------|-----------------------|-----------|",
    ])
    for fp in file_progress:
        lines.append(
            f"| `{fp['file']}` | {fp['lang']} | {fp['filled']} / {fp['total']} | {fp['total'] - fp['filled']} |"
        )

    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def get_translatable_mask(df):
    return (
        df["english"].fillna("").str.strip().ne("")
        & ~df["tag"].isin(EXCLUDED_TAGS)
    )


def scan_all_progress(dict_files):
    progress = []
    for filepath in dict_files:
        fn = os.path.basename(filepath)
        lang_code = fn.replace("dictionary_", "").replace(".csv", "")
        df = pd.read_csv(filepath, dtype=str)
        t_mask = get_translatable_mask(df)
        filled_mask = t_mask & df["claude"].fillna("").str.strip().ne("")
        progress.append({
            "file": fn,
            "lang": LANG_NAMES.get(lang_code, lang_code),
            "filled": int(filled_mask.sum()),
            "total": int(t_mask.sum()),
        })
    return progress


def main():
    specific_lang = sys.argv[1] if len(sys.argv) > 1 else None
    all_files = sorted(glob.glob(os.path.join(DB_DIR, "dictionary_*.csv")))
    dict_files = [f for f in all_files if not f.endswith("dictionary_reference.csv")]

    if specific_lang:
        target_files = [f for f in dict_files if f.endswith(f"dictionary_{specific_lang}.csv")]
        if not target_files:
            print(f"No dictionary file found for '{specific_lang}'")
            sys.exit(1)
    else:
        target_files = dict_files

    stats = {
        "calls": 0,
        "translated": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "thinking_tokens": 0,
        "cache_read_tokens": 0,
        "total_tokens": 0,
    }

    stop_info = None
    for idx_f, filepath in enumerate(target_files, 1):
        fn = os.path.basename(filepath)
        lang_code = fn.replace("dictionary_", "").replace(".csv", "")
        target_lang = LANG_NAMES.get(lang_code, lang_code)

        df = pd.read_csv(filepath, dtype=str)
        missing_mask = get_translatable_mask(df) & (df["claude"].isna() | df["claude"].str.strip().eq(""))
        indices = df[missing_mask].index.tolist()

        if not indices:
            print(f"[{idx_f}/{len(target_files)}] {fn}: already complete.")
            continue

        if lang_code == "en":
            for i in indices:
                df.at[i, "claude"] = df.at[i, "english"]
            df.to_csv(filepath, index=False)
            stats["translated"] += len(indices)
            print(f"[{idx_f}/{len(target_files)}] {fn}: mirrored {len(indices)} English rows.")
            continue

        total_batches = (len(indices) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"[{idx_f}/{len(target_files)}] {fn} ({target_lang}): {len(indices)} missing items in {total_batches} batch(es).", flush=True)

        for b_num, start in enumerate(range(0, len(indices), BATCH_SIZE), 1):
            batch_indices = indices[start:start + BATCH_SIZE]
            batch_rows = [df.loc[i].to_dict() for i in batch_indices]
            first_key = str(batch_rows[0].get("key", ""))
            print(f"  Batch {b_num}/{total_batches} ({len(batch_rows)} items, starting at '{first_key}')...", flush=True)

            try:
                translations = translate_batch(batch_rows, target_lang, stats)
            except Exception as e:
                stop_info = {
                    "file": fn,
                    "batch": b_num,
                    "total_batches": total_batches,
                    "first_key": first_key,
                    "reason": str(e),
                }
                print(f"  STOPPED at {fn} batch {b_num}/{total_batches} (key '{first_key}'): {e}", flush=True)
                progress = scan_all_progress(dict_files)
                write_status_doc(progress, stats, stop_info=stop_info)
                sys.exit(1)

            for df_idx, trans in zip(batch_indices, translations):
                df.at[df_idx, "claude"] = trans
            df.to_csv(filepath, index=False)
            stats["translated"] += len(translations)

        progress = scan_all_progress(dict_files)
        write_status_doc(progress, stats, stop_info=None)

    progress = scan_all_progress(dict_files)
    write_status_doc(progress, stats, stop_info=None)
    print(f"\nDone! Translated {stats['translated']} items in {stats['calls']} calls. Status saved to {STATUS_PATH}")


if __name__ == "__main__":
    main()
