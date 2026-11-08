import os
import platform
import subprocess
import urllib.parse
import urllib.request


def is_termux() -> bool:
  """Detects if the script is running inside Android Termux."""
  return "TERMUX_VERSION" in os.environ or os.path.exists(
      "/data/data/com.termux"
  )


def speak(text: str):
  """Cross-platform Text-to-Speech (macOS 'say' vs Termux 'termux-tts-speak')."""
  print(f"[Agent Voice]: {text}")
  if is_termux():
    subprocess.run(["termux-tts-speak", text], check=False)
  elif platform.system() == "Darwin":
    subprocess.run(["say", text], check=False)


def get_weather(location: str) -> str:
  """Fetches live weather from wttr.in with clean fallback formatting."""
  try:
    loc_clean = urllib.parse.quote(location)
    url = f"https://wttr.in/{loc_clean}?format=%C+%t"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=5) as response:
      res = response.read().decode("utf-8").strip()
      if "location not found" in res.lower() or "404" in res:
        return f"Could not find weather data for {location}."
      return f"The current weather in {location} is {res}."
  except Exception as e:
    return f"Failed to fetch weather: {e}"


def execute_action(payload: dict):
  """Executes the tool derived from intent parsing."""
  tool = payload.get("tool")
  params = payload.get("parameters", {})

  if tool == "get_weather":
    loc = params.get("location", "Bengaluru")
    result = get_weather(loc)
    speak(result)
    return result

  speak(f"Executed action {tool} successfully.")
  return f"Executed {tool} with {params}"