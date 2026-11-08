import os
import subprocess
from agent_brain import parse_intent_to_tool
from live_agent import TOOL_REGISTRY


def run_voice_pipeline():
  audio_path = "fixed_audio.wav"
  model_path = "ggml-tiny.bin"

  print("=== Starting End-to-End Voice Agent Pipeline ===")

  # Step 1: Speech-to-Text
  if not os.path.exists(audio_path):
    print(f"[Error]: Missing audio file '{audio_path}'")
    return

  print("1. Transcribing audio with whisper-cli...")
  cmd = ["whisper-cli", "-m", model_path, "-f", audio_path, "-nt"]
  result = subprocess.run(cmd, capture_output=True, text=True, check=True)
  transcript = result.stdout.strip()
  print(f"   -> User Spoke: \"{transcript}\"")

  # Step 2: Intent Parsing (Brain)
  print("2. Parsing intent into tool payload...")
  payload = parse_intent_to_tool(transcript)
  print(f"   -> Generated Payload: {payload}")

  # Step 3: Tool Execution
  tool_name = payload.get("tool")
  params = payload.get("parameters", {})

  if tool_name in TOOL_REGISTRY:
    print(f"3. Executing tool '{tool_name}'...")
    TOOL_REGISTRY[tool_name](params)
    print("   -> Execution Complete Successfully!")
  else:
    print(f"3. [Notice]: Could not map intent to a valid tool.")


if __name__ == "__main__":
  run_voice_pipeline()