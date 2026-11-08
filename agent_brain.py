import json
from llama_cpp import Llama

# Load the local LLM model once
print("[Brain] Loading local Qwen model...")
llm = Llama(
    model_path="qwen0.5b.gguf",
    n_ctx=512,
    verbose=False,
)

# Alias map for common phonetic transcription misspellings
CITY_ALIASES = {
    "bingloru": "Bengaluru",
    "banglore": "Bengaluru",
    "bangalore": "Bengaluru",
    "gloru": "Bengaluru",
    "hyderbad": "Hyderabad",
    "delhi": "New Delhi",
}


def normalize_parameters(tool: str, params: dict) -> dict:
  """Normalizes parameters to fix speech-to-text typos before tool execution."""
  if tool == "get_weather" and "location" in params:
    raw_location = str(params["location"]).strip()
    loc_lower = raw_location.lower()

    # Check for alias matches
    for key, mapped_city in CITY_ALIASES.items():
      if key in loc_lower:
        params["location"] = mapped_city
        return params

    # Clean up trailing filler words if present
    clean_loc = raw_location.replace(" currently", "").strip(" ?.")
    params["location"] = clean_loc.title()

  return params


def parse_intent_to_tool(transcript: str) -> dict:
  """Uses local Qwen model to parse transcript and normalizes entity outputs."""
  system_prompt = (
      "You are the brain of an offline voice assistant. Your job is to read"
      " the user transcript and map it strictly to one of these tools: "
      "1. get_weather (parameters: location)\n"
      "2. whatsapp_message (parameters: phone, message)\n"
      "3. calendar_event (parameters: title, datetime)\n"
      "4. chrome_browse (parameters: url)\n"
      "5. file_manager (parameters: action, path, content)\n\n"
      "Return ONLY a valid JSON object matching this structure, with no extra"
      ' text or markdown formatting:\n{"tool": "tool_name", "parameters":'
      ' {"key": "value"}}'
  )

  user_prompt = f"User said: '{transcript}'"

  try:
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        max_tokens=100,
    )

    content = response["choices"][0]["message"]["content"].strip()

    # Clean markdown formatting if present
    if content.startswith("```"):
      content = content.split("```")[1]
      if content.startswith("json"):
        content = content[4:]
    content = content.strip()

    parsed = json.loads(content)
    tool_name = parsed.get("tool", "unknown")
    params = parsed.get("parameters", {})

    # Apply parameter normalization
    normalized_params = normalize_parameters(tool_name, params)
    return {"tool": tool_name, "parameters": normalized_params}

  except Exception as e:
    print(f"[Brain Error]: {e}")
    return {"tool": "unknown", "parameters": {}}