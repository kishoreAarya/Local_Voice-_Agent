#!/bin/bash
set -e

echo "=== Setting up Local Voice Agent on Termux ==="

pkg update -y
pkg install -y git cmake clang make python termux-api curl

if [ ! -d "$HOME/whisper.cpp" ]; then
    echo "Cloning and building whisper.cpp..."
    git clone https://github.com/ggerganov/whisper.cpp.git "$HOME/whisper.cpp"
    cd "$HOME/whisper.cpp"
    cmake -B build
    cmake --build build --config Release
    cd -
fi

if [ ! -f "$HOME/whisper.cpp/ggml-tiny.bin" ]; then
    echo "Downloading ggml-tiny.bin model..."
    curl -L -C - -o "$HOME/whisper.cpp/ggml-tiny.bin" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin
fi

ln -sf "$HOME/whisper.cpp/build/bin/whisper-cli" ./whisper-cli
ln -sf "$HOME/whisper.cpp/ggml-tiny.bin" ./ggml-tiny.bin

if [ ! -f "./qwen0.5b.gguf" ]; then
    echo "Downloading Qwen2.5-0.5B model..."
    curl -L -C - -o qwen0.5b.gguf https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf
fi

echo "=== Setup Complete! You are ready to run the Voice Agent. ==="
