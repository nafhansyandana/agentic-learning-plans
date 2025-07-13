import json
import os

DATA_FILE = "data/saved_plan.json"

def save_plan(subtopics: str, plan: str):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok = True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"subtopics": subtopics, "plan": plan}, f, indent = 2)

def load_plan():
    if not os.path.exists(DATA_FILE):
        return None, None
    with open(DATA_FILE, "r", encoding = "utf-8") as f:
        data = json.load(f)
    return data.get("subtopics", ""), data.get("plan", "")

def reset_plan():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
