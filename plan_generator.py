import json
import os
from fpdf import FPDF
from io import BytesIO

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

def generate_pdf(content: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    # Add a Unicode capable font (DejaVuSans)
    font_path = os.path.join("assets", "fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni = True)
    pdf.set_font("DejaVu", size = 12)

    for line in content.splitlines():
        pdf.multi_cell(0, 10, line)

    temp_path = "temp_output.pdf"
    pdf.output(temp_path)

    with open(temp_path, "rb") as f:
        pdf_bytes = f.read()

    os.remove(temp_path)
    return pdf_bytes
