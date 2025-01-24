#!/usr/bin/python3
import socket
from piper_play import *

def receive_udp_message(port):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("", port))
        print(f"Listening for UDP messages on port {port}...")
        data, addr = udp_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        print("Received message: " + data.decode(“utf-8”))
        udp_socket.close()
        return data.decode(“utf-8”)

    except Exception as e:
        print(f"Error receiving UDP message: {e}")

def main():
    voix = “female”
    target_port = 8888       # Replace with the target port number
    while True:
        msg=receive_udp_message(target_port)
        piper_play(msg,voix)

main()
