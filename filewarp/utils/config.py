from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().home()

OUTPUT_DIR = BASE_DIR / "Documents"

CACHE_DIR = BASE_DIR / "tmp/filewarp"

# Ensure cache dir exists
os.makedirs(CACHE_DIR, exist_ok=True)
