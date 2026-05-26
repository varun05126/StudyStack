import re
from PyPDF2 import PdfReader
from docx import Document


# ---------- TEXT EXTRACTION ----------

def extract_text(file):
    name = file.name.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif name.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")

    elif name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return ""


# ---------- DIFFICULTY ENGINE ----------

HARD_WORDS = [
    "algorithm", "theorem", "proof", "derivation", "complexity",
    "neural", "regression", "integration", "differential",
    "optimization", "compiler", "cryptography", "architecture",
    "machine learning", "deep learning", "probability", "statistics"
]

def estimate_difficulty(text):
    text = text.lower()
    words = re.findall(r"\b\w+\b", text)
    length = len(words)

    score = 0
    for w in HARD_WORDS:
        if w in text:
            score += 2

    if length > 3000:
        score += 4
    elif length > 1500:
        score += 3
    elif length > 700:
        score += 2
    elif length > 300:
        score += 1

    if score <= 1:
        return 1
    elif score <= 3:
        return 2
    elif score <= 5:
        return 3
    elif score <= 7:
        return 4
    else:
        return 5
