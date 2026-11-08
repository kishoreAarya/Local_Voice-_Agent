import subprocess


def transcribe_audio(audio_path: str, model_path: str = "models/ggml-tiny.bin") -> str:
  """Transcribes a local .wav audio file into text using whisper.cpp."""
  print(f"[STT] Transcribing {audio_path} using model {model_path}...")

  try:
    # Construct whisper-cpp command (adjust binary name if compiling from source)
    cmd = ["whisper-cpp", "-m", model_path, "-f", audio_path, "-nt"]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    transcript = result.stdout.strip()
    print(f"[STT] Result: {transcript}")
    return transcript
  except subprocess.CalledProcessError as e:
    print(f"[STT Error]: {e.stderr}")
    return ""
  except FileNotFoundError:
    print("[STT Error]: whisper-cpp binary not found. Please install it.")
    return ""


if __name__ == "__main__":
  # Quick test with a dummy or sample audio file if available
  print("STT Bridge module loaded successfully.")