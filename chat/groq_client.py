import os
from django.conf import settings
from groq import Groq

_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in your .env file.")
        _client = Groq(api_key=api_key)
    return _client

def generate_reply(history):
    import time
    client = _get_client()

    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ]

    last_error = None
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as exc:
            last_error = exc
            if "429" in str(exc) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            break

    raise last_error