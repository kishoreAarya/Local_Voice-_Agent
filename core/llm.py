import json
import requests

URL = "http://localhost:8080/v1/chat/completions"

TOOLS = ["get_weather", "whatsapp_message", "calendar_event",
         "chrome_browse", "file_manager", "speak"]

SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {"type": "string", "enum": TOOLS},
        "parameters": {"type": "object"},
    },
    "required": ["tool", "parameters"],
}

SYSTEM = """You are a voice assistant. Reply ONLY with a JSON tool call.
Tools and parameters:
- get_weather: {"location": str}
- whatsapp_message: {"phone": str, "message": str}
- calendar_event: {"title": str, "datetime": str}
- chrome_browse: {"url": str}
- file_manager: {"action": "read"|"write"|"list", "path": str, "content": str}
- speak: {"text": str}  (use for questions, chat, or when no other tool fits)
Keep spoken text short.
-Speak like a warm, friendly person. Use short natural sentences, contractions, and varied punctuation (commas, question marks, exclamation marks). No lists or emojis.
"""


def ask(user_text: str, history=None) -> dict:
    messages = [{"role": "system", "content": SYSTEM}]
    messages += history or []
    messages.append({"role": "user", "content": user_text})
    r = requests.post(URL, json={
        "messages": messages,
        "temperature": 0.2,
        "response_format": {"type": "json_object", "schema": SCHEMA},
    }, timeout=120)
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"tool": "speak", "parameters": {"text": content}}


if __name__ == "__main__":
    for q in ["weather in Nellore", "what is 2 plus 2",
              "open youtube", "message +919876543210 I'll be late"]:
        print(q, "->", ask(q))