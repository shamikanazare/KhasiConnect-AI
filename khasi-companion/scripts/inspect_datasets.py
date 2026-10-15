import os
import sys
from pathlib import Path
import pandas as pd

# Ensure Windows console supports UTF-8 characters and emojis
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def inspect_local_dataset_folder(folder_path: str = "data/raw_datasets"):
    """
    Scans a folder shared by teammates, prints every file found, and inspects
    tabular files (CSV, TSV, XLSX, JSON, Parquet) for columns, row counts,
    empty values, duplicates, and sample rows.
    """
    base = Path(folder_path)
    if not base.exists():
        print(f"[!] Folder '{folder_path}' does not exist yet. Creating it now...")
        base.mkdir(parents=True, exist_ok=True)
        print(f"--> Please place your shared dataset files inside '{folder_path}' and run this again.")
        return

    all_files = [p for p in base.rglob("*") if p.is_file() and not p.name.startswith(".")]
    if not all_files:
        print(f"[INFO] The folder '{folder_path}' is currently empty.")
        print("--> Copy or upload your dataset folder into 'data/raw_datasets/' and re-run!")
        return

    print(f"=== Found {len(all_files)} file(s) in '{folder_path}' ===\n")

    audio_extensions = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
    audio_count = 0

    for file_path in all_files:
        ext = file_path.suffix.lower()
        if ext in audio_extensions:
            audio_count += 1
            continue

        print("--------------------------------------------------")
        print(f"File: {file_path.relative_to(base)} ({file_path.stat().st_size / 1024:.1f} KB)")
        try:
            if ext == ".csv":
                df = pd.read_csv(file_path)
            elif ext == ".tsv":
                df = pd.read_csv(file_path, sep="\t")
            elif ext in {".xls", ".xlsx"}:
                df = pd.read_excel(file_path)
            elif ext == ".json":
                df = pd.read_json(file_path)
            elif ext == ".jsonl":
                df = pd.read_json(file_path, lines=True)
            elif ext == ".parquet":
                df = pd.read_parquet(file_path)
            else:
                print(f"   [Skipped table preview for extension '{ext}']")
                continue

            print(f"   [+] Total Rows: {len(df):,}")
            print(f"   [+] Columns: {list(df.columns)}")
            print(f"   [?] Missing / Null Values per column:\n{df.isnull().sum().to_dict()}")
            print(f"   [?] Exact Duplicate Rows: {df.duplicated().sum():,}")
            print(f"   [*] First 3 Sample Rows:")
            print(df.head(3).to_string(index=False))
            print()
        except Exception as e:
            print(f"   [-] Could not read '{file_path.name}' automatically: {e}\n")

    if audio_count > 0:
        print(f"[AUDIO] Detected {audio_count} audio file(s) for ASR/TTS evaluation!")

if __name__ == "__main__":
    inspect_local_dataset_folder("data/raw_datasets")
