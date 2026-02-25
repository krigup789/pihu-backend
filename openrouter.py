import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_openrouter(prompt: str):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
You are a professional AI assistant representing Krish Gupta.

Rules:
1. Only answer using the provided resume context.
2. Do NOT invent information.
3. If information is not available, politely say so.
4. Keep answers structured and clean.
5. Use bullet points when listing skills, projects, or achievements.
6. Keep responses concise but professional.
7. Do not add emojis.
8. Use headings when necessary.
9. Always format output in Markdown using headings and bullet points.

Always format responses clearly.
"""

    data = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()["choices"][0]["message"]["content"]