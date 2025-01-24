#!/usr/bin/python3
import serial, tempfile, os
from piper_play import *
# Configuration
SERIAL_PORT = "/dev/ttyUSB0"   # or for GPIO: /dev/ttyS2
BAUD_RATE = 9600

def main():
    try:
        # Open serial port
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening for messages on {SERIAL_PORT} at {BAUD_RATE} baud.")
            while True:
                # Read a line of data from the serial port
                if ser.in_waiting > 0:
                    mes = ser.readline().decode('utf-8').strip()
                    mes = mes + "\n"
                    print(f"Received: {mes}")
                    piper_play(mes,"female")
    except serial.SerialException as e:
        print(f"Error: {e}")

main()

