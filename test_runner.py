import json
from live_agent import TOOL_REGISTRY

# 1. Define sample payloads for all registered tools
MOCK_PAYLOADS = [
    {
        "test_name": "Weather Tool Test",
        "payload": {
            "tool": "get_weather",
            "parameters": {"location": "Bengaluru"},
        },
    },
    {
        "test_name": "WhatsApp Link Test",
        "payload": {
            "tool": "whatsapp_message",
            "parameters": {
                "phone": "+919876543210",
                "message": "Testing agent from laptop!",
            },
        },
    },
    {
        "test_name": "Calendar Log Test",
        "payload": {
            "tool": "calendar_event",
            "parameters": {
                "title": "Architecture Review",
                "datetime": "2026-11-10 14:00",
            },
        },
    },
    {
        "test_name": "Chrome Launch Test",
        "payload": {
            "tool": "chrome_browse",
            "parameters": {"url": "https://github.com"},
        },
    },
    {
        "test_name": "File Manager Write Test",
        "payload": {
            "tool": "file_manager",
            "parameters": {
                "action": "write",
                "path": "laptop_test.txt",
                "content": "Laptop execution verified successfully.",
            },
        },
    },
]


def run_unit_tests():
  print("=" * 50)
  print(" RUNNING LOCAL AGENT TOOL LOGIC TESTS ")
  print("=" * 50)

  for idx, test in enumerate(MOCK_PAYLOADS, 1):
    print(f"\n[Test {idx}/5]: {test['test_name']}")
    data = test["payload"]
    tool_name = data.get("tool")
    params = data.get("parameters", {})

    if tool_name in TOOL_REGISTRY:
      try:
        print(f" -> Executing '{tool_name}' with parameters: {params}")
        TOOL_REGISTRY[tool_name](params)
        print(f" -> Result: SUCCESS")
      except Exception as e:
        print(f" -> Result: FAILED with error: {e}")
    else:
      print(f" -> Result: FAILED (Tool '{tool_name}' not found in registry)")

  print("\n" + "=" * 50)
  print(" ALL TESTS COMPLETED ")
  print("=" * 50)


if __name__ == "__main__":
  run_unit_tests()