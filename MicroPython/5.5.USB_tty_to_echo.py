#python3 USB_to_stdout.py | ./piper -m models/GB/female.onnx --output-raw | \
# aplay -r 16000 -f S16_LE -t raw -

#!/usr/bin/python3
import serial, tempfile, os

# Configuration
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

try:
    # Open serial port
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Listening for messages on {SERIAL_PORT} at {BAUD_RATE} baud.")
        while True:
            # Read a line of data from the serial port
            if ser.in_waiting > 0:
                message = ser.readline().decode('utf-8').strip()
                message = message + "\n"
                print(f"Received: {message}")
                                # Write the message to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, mode='w', prefix='usb_message_', suffix='.txt') as temp_file:
                    temp_file.write(message)
                    print(f"Message written to temporary file: {temp_file.name}")

                # Read back from the temporary file and use echo command
                with open(temp_file.name, 'r') as file:
                    file_content = file.read()
                    print(f"Read from temporary file: {file_content}")
                    os.remove(temp_file.name)
                    os.system(f'echo "{file_content}"')

except serial.SerialException as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    
    