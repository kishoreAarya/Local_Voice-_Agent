from pathlib import Path
from urllib.parse import quote

import requests

from adapters import open_url, speak
from core import db
from core.llm import ask

SANDBOX = Path("output").resolve()
SANDBOX.mkdir(exist_ok=True)


def _safe(path: str) -> Path:
    p = (SANDBOX / path).resolve()
    if p != SANDBOX and SANDBOX not in p.parents:
        raise ValueError("Path is outside the allowed folder")
    return p


def get_weather(location="Hyderabad"):
    r = requests.get(f"https://wttr.in/{quote(location)}?format=3", timeout=10)
    r.raise_for_status()
    return r.text.strip()


def whatsapp_message(phone, message):
    open_url(f"https://wa.me/{phone.lstrip('+')}?text={quote(message)}")
    return f"Opening WhatsApp for {phone}. Tap send to confirm."


def calendar_event(title, datetime):
    db.add_event(title, datetime)
    return f"Saved {title} for {datetime}."


def chrome_browse(url):
    if not url.startswith(("http://", "https://")):
        raise ValueError("Only http and https links are allowed")
    open_url(url)
    return "Opening the page."


def file_manager(action, path, content=""):
    p = _safe(path)
    if action == "read":
        return p.read_text()[:500]
    if action == "write":
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"Wrote {path}."
    if action == "list":
        return ", ".join(x.name for x in p.iterdir()) or "Folder is empty."
    raise ValueError(f"Unknown action {action}")


def speak_tool(text):
    return text


TOOLS = {
    "get_weather": get_weather,
    "whatsapp_message": whatsapp_message,
    "calendar_event": calendar_event,
    "chrome_browse": chrome_browse,
    "file_manager": file_manager,
    "speak": speak_tool,
}


def dispatch(call: dict, session_id: int) -> str:
    tool, params = call.get("tool"), call.get("parameters", {})
    try:
        result = TOOLS[tool](**params)
        db.log_action(session_id, tool, params, result, True)
        return result
    except Exception as e:
        msg = f"Sorry, {tool} failed: {e}"
        db.log_action(session_id, tool, params, msg, False)
        return msg


if __name__ == "__main__":
    db.init()
    sid = db.new_session()
    while True:
        text = input("you> ").strip()
        if text in ("q", "quit", "exit"):
            break
        db.log_message(sid, "user", text)
        reply = dispatch(ask(text), sid)
        db.log_message(sid, "assistant", reply)
        print("agent>", reply)
        speak(reply)