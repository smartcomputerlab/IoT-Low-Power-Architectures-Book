#./whisper -m models/ggml-tiny.en.bin -c 1 -t 8 –step 2000 –length 8000 -kc -ac 1024 -vth 0.5 | \
#./stdout_filter_tty.py

#!/usr/bin/python3

import serial
import sys
import re

def filter_string(input_string):
    pattern = bytes.fromhex("201b5b324b0d20").decode('latin1')
    start_index = input_string.rfind(pattern)
    if start_index == -1:
        return ""
    return input_string[start_index+7:]  # starting after the token

def main():
    try:
        # Configure the serial port
        serial_port = "/dev/ttyS2"  # Replace with your specific serial port
        baud_rate = 9600  # You can adjust this based on your requirements
        # Open the serial port
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print(f"Opened serial port {serial_port} at baud rate {baud_rate}")
            print("Type your message below and press Enter to send:")
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
                    ser.write(result.encode('utf-8'))
                    print("sent")
                else:
                    print("not sent")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    