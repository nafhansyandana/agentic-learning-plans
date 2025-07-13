import json
import os
from datetime import datetime

DATA_FILE = "data/progress_log.json"

def save_progress_note(note: str):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok = True)
    logs = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding = "utf-8") as f:
            logs = json.load(f)
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "note": note
    })
    with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump(logs, f, indent=2)

def load_progress_notes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding = "utf-8") as f:
        return json.load(f)

def reset_progress_notes():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
