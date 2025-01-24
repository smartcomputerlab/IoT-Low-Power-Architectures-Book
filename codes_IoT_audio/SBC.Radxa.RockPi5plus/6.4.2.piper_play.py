#!/usr/bin/python3
import  os

def piper_play(msg, voice):
        msg = msg + "\n"
        print(f"Received message: {msg}")
        os.system(f'echo "{msg}" | ./piper -m models/{voice}.onnx --output-raw | \
        aplay -r 16000 -f S16_LE -t raw -')
        