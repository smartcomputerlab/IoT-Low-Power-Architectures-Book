import time, ustruct
from machine import I2C, Pin, UART
import lora_init

lora = lora_init.lora_init()

def send_lora_data(buffer):
    try:
        # Create the message with temperature, humidity, and luminosity
        #message = f"T:{temperature:.2f},H:{humidity:.2f},L:{luminosity:.2f}"
        #print("Sending LoRa packet:", buffer)
        # prepare data packet with bytes
        data = ustruct.pack('8s128s','AI_lab: ',buffer)
        # Convert message to bytes
        # lora.println(bytes(message, 'utf-8'))
        if buffer != b'None':
            lora.println(buffer)
            print(buffer.decode('utf-8'))
    except Exception as e:
        print("Failed to send LoRa packet:", e)

# Main program
def main():
    #led = Pin (8, Pin.OUT)
    uart = UART(1, baudrate=9600, rx=1, tx=0)
    # Initialize LoRa communication
    while 1:
        if uart.any():
            time.sleep(0.1)
            message = uart.readline().decode('utf-8').strip()
            uart.flush()
            #print(message)
            send_lora_data(message.encode('utf-8'))
    # Run the main program
main()
