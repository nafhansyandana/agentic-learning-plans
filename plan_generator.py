import json
import os

BASE_DIR = "data/users"

def _user_plan_file(username: str) -> str:
    return os.path.join(BASE_DIR, username, "plan.json")

def save_plan(username: str, subtopics: str, plan: str):
    path = _user_plan_file(username)
    os.makedirs(os.path.dirname(path), exist_ok = True)
    with open(path, "w", encoding = "utf-8") as f:
        json.dump({"subtopics": subtopics, "plan": plan}, f, indent = 2)

def load_plan(username: str):
    path = _user_plan_file(username)
    if not os.path.exists(path):
        return None, None
    with open(path, "r", encoding = "utf-8") as f:
        data = json.load(f)
    return data.get("subtopics", ""), data.get("plan", "")

def reset_plan(username: str):
    path = _user_plan_file(username)
    if os.path.exists(path):
        os.remove(path)

def prepare_download_content(content: str) -> bytes:
    return content.encode("utf-8")
