# Local Voice-to-Voice AI Agent: System Architecture

## 1. High-Level System Overview
The Voice-to-Voice AI Agent is an edge-native, privacy-focused automation assistant designed to run on Android hardware (via Termux and native system integrations). It transforms human audio input into system actions, external API integrations, and synthesized speech responses.

```
+-----------------------------------------------------------------------------------+
|                                 USER / ENVIRONMENT                                |
+-----------------------------------------------------------------------------------+
       | (Human Audio Speech)                                ▲ (Synthesized Audio)
       v                                                     |
+-------------------+                               +-------------------+
|  1. PERCEPTION    |                               |  4. VOICE OUTPUT  |
| - Mic Capture     |                               | - Android TTS     |
| - Whisper.cpp STT |                               | - Piper / Google  |
+-------------------+                               +-------------------+
       | (Transcribed Text)                                  ▲ (Voice Text)
       v                                                     |
+-----------------------------------------------------------------------------------+
|                             2. ORCHESTRATION & BRAIN                              |
| - Local LLM Engine (llama.cpp / Qwen 2.5 3B / MiniCPM GGUF)                       |
| - System Prompt & JSON Tool Schema Parser                                         |
+-----------------------------------------------------------------------------------+
       | (Structured JSON Tool Call Payload)                 ▲ (Execution Results)
       v                                                     |
+-----------------------------------------------------------------------------------+
|                              3. ACTION & EXECUTION                                |
| - Tool Dispatcher Registry (live_agent.py)                                        |
| - Integrations: WhatsApp (wa.me), Google Calendar, Chrome, File System, Calls     |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
|                            5. PERSISTENCE & STATE                                 |
| - SQLite Database (Session Context, Conversation History, Action Auditing Logs)   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Layer Specifications

### Layer 1: Perception (Speech-to-Text)
* **Component:** `whisper.cpp` (ARM64 optimized build).
* **Model:** `ggml-tiny.en.bin` or `ggml-base.en.bin`.
* **Audio Capture:** `termux-microphone-record` or Python `wave`/`sounddevice` writing to `/tmp/input.wav`.
* **Output:** Clean string transcription emitted to stdin/dispatcher.

### Layer 2: Orchestration & Brain (LLM & Tool Selection)
* **Component:** `llama-cli` / `llama.cpp` server (GGUF Quantization Q4_K_M).
* **Target Models:** MiniCPM-2B / Qwen-2.5-3B-Instruct.
* **Context Budget:** Strict maximum limit of 2048 tokens.
* **Function Routing:** Zero-shot JSON tool generation enforcing strict formatting schema:
  `{"tool": "<tool_name>", "parameters": {...}}`

### Layer 3: Action & Execution (System Hooks)
* **Dispatcher Script:** Python-based module host (`live_agent.py`).
* **Tool Modules:**
  * **Weather:** `wttr.in` API over `curl`/`requests`.
  * **WhatsApp:** Android URI intents (`https://wa.me/<phone>?text=<msg>`).
  * **Chrome/Web:** `termux-open-url` / `webbrowser` launcher.
  * **Calendar/Notes:** Local structured logs (`calendar_log.txt` / SQLite database).
  * **File System:** Native Python `os`, `shutil`, `pathlib` APIs.

### Layer 4: Voice & Speech Output (Text-to-Speech)
* **Engine:** `termux-tts-speak` (Native Android TTS engine) or Google Web TTS fallback.
* **Format:** Raw string payload converted to speech without block characters.

### Layer 5: State & Memory Management
* **Engine:** SQLite (`agent_state.db`).
* **Tables:** `sessions`, `messages`, `action_logs`.
* **Purpose:** Audit tracking, session recovery, and context injection.