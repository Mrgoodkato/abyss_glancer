from pathlib import Path

# 1. Get the absolute path of the directory containing THIS current file
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Append your folder names to the base directory
RAW_SAVE_DIR = BASE_DIR / "fetched_data"
PARSED_SAVE_DIR = BASE_DIR / "parsed_data"