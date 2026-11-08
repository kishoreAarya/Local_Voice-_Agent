import os
import subprocess
import tempfile

VOICE = "models/voices/en_US-amy-medium.onnx"


def speak(text: str):
    if os.path.exists(VOICE):
        try:
            out = os.path.join(tempfile.gettempdir(), "agent_tts.wav")
            subprocess.run(["piper", "-m", VOICE, "-f", out],
                           input=text.encode(), check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["afplay", out])
            return
        except Exception:
            pass
    subprocess.run(["say", text])


def open_url(url: str):
    subprocess.run(["open", url])


def record(wav_path: str, device: str = ":1"):
    """Push-to-talk: Enter to start, Enter to stop. Writes 16 kHz mono WAV."""
    input("  [Enter] to start talking...")
    p = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "avfoundation",
         "-i", device, "-ar", "16000", "-ac", "1", wav_path],
        stdin=subprocess.PIPE)
    input("  Listening... [Enter] to stop")
    p.communicate(b"q")
