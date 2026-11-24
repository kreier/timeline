#!/usr/bin/env python3
"""
Synchronize English references and fill Gemini translations across all db/dictionary_*.csv files.
"""

import os
import sys
import time
import re
import glob
import pandas as pd
from google import genai

sys.stdout.reconfigure(line_buffering=True)

# Load environment variables from .env
def load_dotenv(dotenv_path):
    if os.path.isfile(dotenv_path):
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if k and not os.getenv(k):
                        os.environ[k] = v

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY is not set.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY, http_options={"timeout": 20000})
MODEL_NAME = "gemini-3.1-flash-lite"
BATCH_SIZE = 40
DELAY_BETWEEN_CALLS = 4.2  # Maintain safe rate under 15 RPM free tier limit

# Language mapping
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

def translate_batch(sources, target_lang, max_retries=5):
    if not sources:
        return []
    numbered = [f"{i+1}. {s}" for i, s in enumerate(sources)]
    prompt = (
        f"You are a professional translator translating a timeline of biblical and world history into {target_lang}.\n"
        f"Translate each numbered item accurately. Maintain Biblical names and terminology according to established usage in {target_lang}.\n"
        f"Return EXACTLY {len(sources)} lines, each beginning with its number followed by a period and space (e.g. \"1. ...\").\n"
        f"Do not omit any items. Do not include markdown bolding, introductory remarks, or explanatory notes.\n\n"
        + "\n".join(numbered)
    )

    for attempt in range(max_retries):
        try:
            resp = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            time.sleep(DELAY_BETWEEN_CALLS)
            lines = [ln.strip() for ln in str(resp.text).splitlines() if ln.strip()]
            parsed = {}
            for ln in lines:
                m = re.match(r"^(\d+)\.\s*(.*)$", ln)
                if m:
                    parsed[int(m.group(1))] = m.group(2).strip()
            if len(parsed) == len(sources) and set(parsed.keys()) == set(range(1, len(sources) + 1)):
                return [parsed[i] for i in range(1, len(sources) + 1)]
            print(f"      [Parse retry {attempt+1}] expected {len(sources)}, parsed {len(parsed)}", flush=True)
        except Exception as e:
            err = str(e)
            wait = 5 * (attempt + 1)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                wait = 25  # Respect free tier sliding window
            elif "503" in err:
                wait = 10
            print(f"      [API retry {attempt+1}] error: {err[:80]} - waiting {wait}s...", flush=True)
            time.sleep(wait)

    if len(sources) > 1:
        print(f"      Splitting batch of {len(sources)} into two halves...", flush=True)
        mid = len(sources) // 2
        left = translate_batch(sources[:mid], target_lang, max_retries)
        right = translate_batch(sources[mid:], target_lang, max_retries)
        return left + right
    else:
        return sources

def process_file(filepath, ref_df, dry_run=False):
    filename = os.path.basename(filepath)
    lang_code = filename.replace("dictionary_", "").replace(".csv", "")
    target_lang = LANG_NAMES.get(lang_code, lang_code)

    df = pd.read_csv(filepath, dtype=str)

    # 1. Parallel Check of English text against dictionary_reference.csv
    mismatches = []
    ref_map = ref_df.set_index("key")["english"].fillna("").to_dict()

    for idx, row in df.iterrows():
        k = row["key"]
        if k in ref_map and k != "daniel2_shift":
            ref_val = ref_map[k]
            curr_val = str(row["english"]) if pd.notna(row["english"]) else ""
            if curr_val != ref_val:
                mismatches.append((k, ref_val, curr_val))
                df.at[idx, "english"] = ref_val
                df.at[idx, "checked"] = "False"
                if k == "version":
                    df.at[idx, "text"] = ref_val

    if mismatches:
        print(f"  [{filename}] Synced {len(mismatches)} English mismatch(es) with reference:")
        for k, r_v, c_v in mismatches[:5]:
            print(f"     Key '{k}': reference={repr(r_v)} vs file={repr(c_v)}")
        if len(mismatches) > 5:
            print(f"     ... and {len(mismatches) - 5} more.")

    # 2. Fill Gemini translation
    if lang_code == "en":
        # For English, gemini column mirrors english text
        mask = (
            df["english"].fillna("").str.strip().ne("") &
            ~df["tag"].isin(["float", "timespan", "deprecated"]) &
            (df["gemini"].isna() | df["gemini"].str.strip().eq(""))
        )
        indices = df[mask].index.tolist()
        for idx in indices:
            df.at[idx, "gemini"] = df.at[idx, "english"]
        if indices:
            print(f"  [{filename}] Populated {len(indices)} rows in English gemini column.")
        if not dry_run:
            df.to_csv(filepath, index=False)
        return len(mismatches), len(indices)

    # Target rows for translation
    mask = (
        df["english"].fillna("").str.strip().ne("") &
        ~df["tag"].isin(["float", "timespan", "deprecated"]) &
        (df["gemini"].isna() | df["gemini"].str.strip().eq(""))
    )
    indices = df[mask].index.tolist()
    sources = df.loc[indices, "english"].tolist()

    if not sources:
        filled_count = (df["gemini"].fillna("").str.strip() != "").sum()
        print(f"  [{filename}] Already completely translated ({filled_count}/511 in gemini).")
        if mismatches and not dry_run:
            df.to_csv(filepath, index=False)
        return len(mismatches), 0

    print(f"  [{filename}] Translating {len(sources)} missing items to {target_lang}...", flush=True)
    t0 = time.time()
    for start in range(0, len(sources), BATCH_SIZE):
        chunk_indices = indices[start:start + BATCH_SIZE]
        chunk = sources[start:start + BATCH_SIZE]
        print(f"    Batch {start // BATCH_SIZE + 1}/{(len(sources) + BATCH_SIZE - 1) // BATCH_SIZE} ({len(chunk)} items)...", flush=True)
        chunk_res = translate_batch(chunk, target_lang)
        for idx, trans in zip(chunk_indices, chunk_res):
            df.at[idx, "gemini"] = trans
        if not dry_run:
            df.to_csv(filepath, index=False)

    dt = time.time() - t0
    filled_count = (df["gemini"].fillna("").str.strip() != "").sum()
    print(f"  [{filename}] Finished in {dt:.1f}s. Total gemini filled: {filled_count}/511.", flush=True)

    return len(mismatches), len(sources)

def main():
    specific_lang = sys.argv[1] if len(sys.argv) > 1 else None

    ref_path = os.path.join(os.path.dirname(__file__), "dictionary_reference.csv")
    ref_df = pd.read_csv(ref_path, dtype=str)

    pattern = os.path.join(os.path.dirname(__file__), "dictionary_*.csv")
    all_files = sorted(glob.glob(pattern))
    dict_files = [f for f in all_files if not f.endswith("dictionary_reference.csv")]

    if specific_lang:
        dict_files = [f for f in dict_files if f.endswith(f"dictionary_{specific_lang}.csv")]
        if not dict_files:
            print(f"No dictionary file found for language '{specific_lang}'")
            sys.exit(1)

    print(f"Found {len(dict_files)} dictionary file(s) to process.")
    total_mismatches = 0
    total_translated = 0

    for i, filepath in enumerate(dict_files, 1):
        fn = os.path.basename(filepath)
        print(f"\n[{i}/{len(dict_files)}] Processing {fn}...")
        m_count, t_count = process_file(filepath, ref_df)
        total_mismatches += m_count
        total_translated += t_count

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Processed {len(dict_files)} dictionary files.")
    print(f"  Total English mismatches synchronized: {total_mismatches}")
    print(f"  Total Gemini translations added: {total_translated}")
    print("=" * 60)

if __name__ == "__main__":
    main()
