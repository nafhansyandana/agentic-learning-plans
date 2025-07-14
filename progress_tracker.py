import json
import os
from datetime import datetime

BASE_DIR = "data/users"

def _user_progress_file(username: str) -> str:
    return os.path.join(BASE_DIR, username, "progress_log.json")

def save_progress_note(username: str, note: str):
    path = _user_progress_file(username)
    os.makedirs(os.path.dirname(path), exist_ok = True)
    logs = []
    if os.path.exists(path):
        with open(path, "r", encoding = "utf-8") as f:
            logs = json.load(f)
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "note": note
    })
    with open(path, "w", encoding = "utf-8") as f:
        json.dump(logs, f, indent = 2)

def load_progress_notes(username: str):
    path = _user_progress_file(username)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding = "utf-8") as f:
        return json.load(f)

def reset_progress_notes(username: str):
    path = _user_progress_file(username)
    if os.path.exists(path):
        os.remove(path)
