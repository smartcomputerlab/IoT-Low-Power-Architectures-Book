import time, ustruct
from machine import Pin, UART
import lora_init

lora = lora_init.lora_init()
    
def send_lora_data(buffer):
    try:
        data = ustruct.pack('8s128s','IoT_lab: ',buffer)
        if buffer != b'None':
            lora.println(buffer)
            print("LoRa packet sent successfully:" +str(buffer))
    except Exception as e:
        print("Failed to send LoRa packet:", e)
        

# Main program
def main():

    uart = UART(1, baudrate=9600, rx=0, tx=1)
    # Initialize LoRa communication
    while 1:
        if uart.any():
            time.sleep(0.1)
            message = uart.readline().decode('utf-8').strip()
            print(message)
            send_lora_data(message.encode('utf-8'))
            #time.sleep(1)
    # Run the main program
main()

