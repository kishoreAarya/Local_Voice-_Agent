# Local Voice-to-Voice AI Agent: Implementation Plan

## Phase 1: Environment Setup & Desktop Development Harness
- [x] Establish architecture (`architecture.md`), design (`design.md`), and plan (`plan.md`).
- [ ] Create laptop workspace with virtual environment (`venv`).
- [ ] Build laptop test harness (`test_harness.py`) to simulate clipboard and voice inputs.
- [ ] Verify tool execution registry (`TOOL_REGISTRY`) against local JSON schemas.

## Phase 2: Speech-to-Text & Local LLM Integration
- [ ] Integrate local audio capture (`wave` / `sounddevice` / `termux-microphone-record`).
- [ ] Download and test `whisper.cpp` (`ggml-tiny.en.bin`) model bindings.
- [ ] Implement system prompt template for zero-shot JSON tool generation.
- [ ] Build fallback handler for direct conversational text to TTS.

## Phase 3: SQLite Persistence Layer
- [ ] Create `agent_state.db` schema initialization script.
- [ ] Implement `log_action(tool_name, params, result)` logging handler.
- [ ] Implement session context retriever to pass recent history to the LLM.

## Phase 4: Mobile Deployment & Testing (Termux Target)
- [ ] Package project files for device deployment (`git` or direct archive transfer).
- [ ] Compile and configure `whisper.cpp` and `llama.cpp` on Termux (ARM64).
- [ ] Verify Android Intent routing (`termux-open-url`, `termux-tts-speak`).
- [ ] Execute full end-to-end voice loop testing on device hardware.