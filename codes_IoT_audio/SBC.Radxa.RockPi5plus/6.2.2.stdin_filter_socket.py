#!/usr/bin/python3
import socket, sys, re
from whisper_filter import *
destination_ip = "192.168.1.32"
#destination_ip = "127.0.0.1"         # to test locally
destination_port = 8888

def send_udp_message(message,ip_address,port):
    try:
        udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.sendto(message.encode(“utf-8”),(ip_address, port))
        udp_socket.close()
        print("UDP package sent")

    except Exception as e:
        print("Error sending UDP package")

def main():
    try:
        while True:
            user_input = input("")
            result = whisper_filter(user_input)
            print(result)
            if result!=None:
                send_udp_message(result,destination_ip,destination_port)
                print("sent")
            else:
                print("not sent")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    