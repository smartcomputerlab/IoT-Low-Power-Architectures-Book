#!/usr/bin/python3
import os
# Callback function for when a message is received
def piper_play(msg,voice):
        msg = msg + "\n"
        print(f"Received message: {msg}")
        os.system(f'echo "{msg}" | ./piper -m models/{voice}.onnx –output-raw | \
        aplay -r 16000 -f S16_LE -t raw -')

def main():
    voix=”female”
    while True:
        message=input("Type new message:")
        on_message(message,voix)

main()

