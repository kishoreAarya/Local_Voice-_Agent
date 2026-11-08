import os
import subprocess


def speak(text: str):
    subprocess.run(["termux-tts-speak", text])


def open_url(url: str):
    subprocess.run(["termux-open-url", url])


def record(wav_path: str, device: str = ""):
    raw = wav_path + ".m4a"
    if os.path.exists(raw):
        os.remove(raw)
    subprocess.run(["termux-microphone-record", "-q"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    input("  [Enter] to start talking...")
    subprocess.run(["termux-microphone-record", "-f", raw, "-l", "0"])
    input("  Listening... [Enter] to stop")
    subprocess.run(["termux-microphone-record", "-q"])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw,
                    "-ar", "16000", "-ac", "1", wav_path])
