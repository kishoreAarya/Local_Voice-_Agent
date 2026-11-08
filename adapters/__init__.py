import os
import platform

PLATFORM = os.environ.get("AGENT_PLATFORM") or (
    "mac" if platform.system() == "Darwin" else "termux")

if PLATFORM == "mac":
    from adapters.mac import speak, open_url, record
else:
    from adapters.termux import speak, open_url, record
