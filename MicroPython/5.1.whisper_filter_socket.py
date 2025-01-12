#!/usr/bin/python3
import socket
import sys
import re

destination_ip = "192.168.1.31"
destination_port = 8888

def send_udp_message(message,ip_address,port):
    try:
        udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.sendto(message.encode(),(ip_address, port))
        udp_socket.close()
        print("UDP package sent")

    except Exception as e:
        print("Error sending UDP package")

def filter_string(input_string):
    pattern = bytes.fromhex("201b5b324b0d20").decode('latin1')
    start_index = input_string.rfind(pattern)
    if start_index == -1:
        return ""
    return input_string[start_index+7:]

def main():
    try:
        while True:
        # Read a string from standard input
            user_input = input("")
            #print(user_input)
            #print(user_input.encode('utf-8').hex())
            result = filter_string(user_input)
            print(result)
            #print(result.encode('utf-8').hex())
            if result.lower() == 'exit':
                print("Exiting program.")
                break
            if result[0:1]!="[" and result[0:1]!="(":
                # Send the input to the serial port
                send_udp_message(result,destination_ip,destination_port)
                print("sent")
            else:
                print("not sent")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    