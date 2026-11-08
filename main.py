from adapters import record, speak
from core import db
from core.dispatcher import dispatch
from core.llm import ask
from core.stt import transcribe

WAV = "/tmp/input.wav"


def main():
    db.init()
    sid = db.new_session()
    history = []
    print("Voice agent ready. Ctrl+C to quit.")
    while True:
        try:
            record(WAV)
        except KeyboardInterrupt:
            break
        text = transcribe(WAV)
        if not text:
            print("  (heard nothing)")
            continue
        print("you>", text)
        db.log_message(sid, "user", text)
        reply = dispatch(ask(text, history[-6:]), sid)
        db.log_message(sid, "assistant", reply)
        history += [{"role": "user", "content": text},
                    {"role": "assistant", "content": reply}]
        print("agent>", reply)
        speak(reply)


if __name__ == "__main__":
    main()
