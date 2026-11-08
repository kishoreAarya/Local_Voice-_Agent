import os
import subprocess


def test_transcription():
  audio_path = "fixed_audio.wav"  # Use the 16kHz converted file
  model_path = "ggml-tiny.bin"

  print(f"[STT Test] Looking for audio file: {audio_path}")
  if not os.path.exists(audio_path):
    print(f"[Notice]: Please ensure '{audio_path}' is in your folder.")
    return

  cmd = ["whisper-cli", "-m", model_path, "-f", audio_path, "-nt"]
  print("[STT Test] Running transcription...")

  try:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(f"\n[Transcription Result]:\n{result.stdout.strip()}\n")
  except subprocess.CalledProcessError as e:
    print(f"[Error Code {e.returncode}]: {e.stderr}")


if __name__ == "__main__":
  test_transcription()