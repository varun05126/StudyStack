import requests
from django.conf import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def extract_topics(goal_title):
    api_key = settings.GROQ_API_KEY

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an academic syllabus designer.

For the learning goal: "{goal_title}"

Return a clean Python-style list of 8–12 core study topics.
Keep topics short and academic.
Do not explain anything.

Example format:
["HTML Basics", "CSS Fundamentals", "JavaScript Basics"]
"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an expert curriculum designer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        text = res.json()["choices"][0]["message"]["content"]

        topics = eval(text)  # AI returns list
        return [t.strip() for t in topics if len(t.strip()) > 2]

    except Exception as e:
        print("Topic extraction error:", e)
        return []
    