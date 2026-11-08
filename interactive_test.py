import json
from live_agent import TOOL_REGISTRY


def interactive_loop():
  print("=== Interactive LLM Output Simulator ===")
  print("Type or paste a raw JSON payload (or type 'exit' to quit):\n")

  while True:
    user_input = input("JSON > ").strip()
    if user_input.lower() == "exit":
      break

    try:
      data = json.loads(user_input)
      tool_name = data.get("tool")
      params = data.get("parameters", {})

      if tool_name in TOOL_REGISTRY:
        print(f"\n[Executing {tool_name}]...")
        TOOL_REGISTRY[tool_name](params)
        print("[Execution Complete]\n")
      else:
        print(f"[Error]: Unknown tool '{tool_name}'\n")
    except json.JSONDecodeError as e:
      print(f"[Invalid JSON]: {e}\n")


if __name__ == "__main__":
  interactive_loop()