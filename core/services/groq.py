import requests
from django.conf import settings

# -------------------------------------------------
# GROQ CONFIG
# -------------------------------------------------

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


# -------------------------------------------------
# CORE GROQ CALLER (SAFE)
# -------------------------------------------------

def call_groq(messages, temperature=0.4):
    api_key = getattr(settings, "GROQ_API_KEY", None)

    if not api_key:
        return "❌ GROQ_API_KEY not found in Django settings."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print("Groq error:", response.text)
            return "⚠️ AI service is temporarily unavailable. Please try again."

        data = response.json()

        if "choices" not in data:
            return "❌ Groq returned unexpected response."

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "❌ Groq API timeout. Please try again."

    except Exception as e:
        return f"❌ Groq API error: {str(e)}"


# -------------------------------------------------
# AI ROADMAP GENERATOR
# -------------------------------------------------

def generate_goal_solution(goal_title: str) -> str:
    """
    Generates a structured AI learning roadmap using Groq.
    """

    messages = [
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
    ]

    return call_groq(messages)


# -------------------------------------------------
# TASK AI ASSISTANT (CHAT MODE)
# -------------------------------------------------

def generate_task_ai_reply(task, user_message: str) -> str:
    """
    Task-aware AI assistant.
    Supports explaining, solving, revising, quizzing.
    """

    system_prompt = f"""
You are a professional study assistant.

Student task:
Title: {task.title}
Subject: {task.custom_subject or task.subject}
Task type: {task.task_type}

Your behavior:
- If it's an assignment: guide step by step, don't just dump answers.
- If it's study: explain simply, then deepen.
- If it's revision: quiz the student.
- If it's exam prep: give strategies + practice questions.

Always be clear, structured, and encouraging.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    return call_groq(messages, temperature=0.5)
