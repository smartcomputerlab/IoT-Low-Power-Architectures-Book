#!/usr/bin/python3
import serial
from piper_play import *
# Configuration
SERIAL_PORT = "/dev/ttyS2"   # on GPIO - or “/dev/ttyUSB0” on USB
BAUD_RATE = 9600

def main():
    voix = "female"
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
                    piper_play(msg,voix)
    except serial.SerialException as e:
        print(f"Error: {e}")

main()
