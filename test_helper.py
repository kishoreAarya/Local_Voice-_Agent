import json
from live_agent import TOOL_REGISTRY

SAMPLE_PAYLOADS = {
    "1": {"tool": "get_weather", "parameters": {"location": "Bengaluru"}},
    "2": {
        "tool": "whatsapp_message",
        "parameters": {
            "phone": "+919876543210",
            "message": "Hello from my AI agent!",
        },
    },
    "3": {
        "tool": "calendar_event",
        "parameters": {
            "title": "Team Sync",
            "datetime": "Tomorrow at 10 AM",
        },
    },
    "4": {"tool": "chrome_browse", "parameters": {"url": "https://github.com"}},
    "5": {
        "tool": "file_manager",
        "parameters": {
            "action": "write",
            "path": "test_output.txt",
            "content": "Laptop development test successful!",
        },
    },
}

if __name__ == "__main__":
  print("=== Laptop Test Harness ===")
  for key, payload in SAMPLE_PAYLOADS.items():
    print(f"[{key}] Test tool: {payload['tool']}")

  choice = input("Select a test tool number (1-5): ").strip()
  if choice in SAMPLE_PAYLOADS:
    data = SAMPLE_PAYLOADS[choice]
    tool_name = data["tool"]
    params = data["parameters"]
    print(f"\n[Executing]: {tool_name} with {params}")
    TOOL_REGISTRY[tool_name](params)
  else:
    print("Invalid selection.")