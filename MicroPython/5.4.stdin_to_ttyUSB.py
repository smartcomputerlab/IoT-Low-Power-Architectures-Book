import serial

# Configuration
SERIAL_PORT = "/dev/ttyUSB0"         # to be adapted 
BAUD_RATE = 9600

try:
    # Open serial port
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Ready to read message from stdin and send to {SERIAL_PORT} at {BAUD_RATE} baud.")
        # Read message character by character until '.'
        message = ""
        print("Type your message : ", end="", flush=True)
        while True:
            message = input()  # Read a single character from stdin
            # Send the message to the serial port
            ser.write(message.encode('utf-8'))
            print(f"Message sent: {message}")
except serial.SerialException as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    