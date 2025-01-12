#!/usr/bin/python3

import socket

def receive_udp_message(port):
    try:
        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the given port
        udp_socket.bind(("", port))
        print(f"Listening for UDP messages on port {port}...")
        # Receive a message
        data, addr = udp_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        print("Received message: " + str(data))
        # Close the socket
        udp_socket.close()

    except Exception as e:
        print(f"Error receiving UDP message: {e}")

def main():
    target_port = 8888       # Replace with the target port number
    # Start receiving messages
    while True:
        receive_udp_message(target_port)

main()
