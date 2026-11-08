import subprocess

MODEL = "models/ggml-tiny.en.bin"


def transcribe(wav_path: str) -> str:
    r = subprocess.run(
        ["whisper-cli", "-m", MODEL, "-f", wav_path, "-nt", "-np"],
        capture_output=True, text=True)
    text = r.stdout.strip()
    if text.startswith("[") and text.endswith("]"):  # [BLANK_AUDIO] etc.
        return ""
    return text
