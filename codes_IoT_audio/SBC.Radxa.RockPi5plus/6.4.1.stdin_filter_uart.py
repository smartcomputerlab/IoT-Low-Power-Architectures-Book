#!/usr/bin/python3
import serial , sys , re
from whisper_filter import *

def main():
    try:
        # Configure the serial port
        serial_port = "/dev/ttyS2"  # Use specific serial port: ttyUSB0 (PC)
        baud_rate = 9600  # You can adjust this based on your requirements
        # Open the serial port
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print(f"Opened serial port {serial_port} at baud rate {baud_rate}")
            print("Type your message below and press Enter to send:")
            while True:
                user_input = input("")
                result = whisper_filter(user_input)
                print(result)
                if result!=None:
                    ser.write(result.encode('utf-8'))
                    print("sent")
                else:
                    print("not sent")
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()
    