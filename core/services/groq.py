import requests
from django.conf import settings

# -------------------------------------------------
# GROQ CONFIG
# -------------------------------------------------

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# -------------------------------------------------
# AI ROADMAP GENERATOR
# -------------------------------------------------

def generate_goal_solution(goal_title: str) -> str:
    """
    Generates a structured AI learning roadmap using Groq.
    """

    api_key = getattr(settings, "GROQ_API_KEY", None)

    if not api_key:
        return "❌ GROQ_API_KEY not found in Django settings."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert learning architect who creates clear, practical learning roadmaps."
            },
            {
                "role": "user",
                "content": f"""
Create a structured learning roadmap for this goal:

{goal_title}

Return clearly in this format:

1. What this goal means
2. Core topics to learn (bullets)
3. Best free resources (YouTube, notes, practice sites)
4. Practice strategy
5. 30-day beginner roadmap
6. How to measure success
"""
            }
        ],
        "temperature": 0.4
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        if "choices" not in data:
            return "❌ Groq API returned unexpected response."

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "❌ Groq API timeout. Please try again."

    except requests.exceptions.HTTPError as e:
        return f"❌ Groq API HTTP error: {str(e)}"

    except Exception as e:
        return f"❌ Groq API error: {str(e)}"
    