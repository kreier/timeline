import pandas as pd
import subprocess
import os
import sys

def run_batch_execution():
    csv_path = '../db/supported_languages.csv'
    script_to_run = '6000.py'
    
    # 1. Check if the files exist before starting
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
        return
    if not os.path.exists(script_to_run):
        print(f"Error: Could not find {script_to_run}")
        return

    # 2. Load the CSV
    df = pd.read_csv(csv_path)

    # 3. Filter for rows where 'dict' is True
    # This handles both boolean True and the string "True"
    valid_langs = df[df['dict'].astype(str).str.lower() == 'true']

    # 4. Extract the 'key' column
    language_codes = valid_langs['key'].tolist()

    print(f"Found {len(language_codes)} languages to process: {language_codes}")

    # 5. Execute the commands
    for lang in language_codes:
        # sys.executable points to D:\archive\github\v13\Scripts\python.exe
        command = [sys.executable, script_to_run, lang, '_nwt']
        print(f"--- Executing: {' '.join(command)} ---")

        try:
            # shell=False is safer; we pass the command as a list
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running {lang}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_batch_execution()
