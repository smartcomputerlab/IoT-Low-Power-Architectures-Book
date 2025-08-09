import time, ustruct
from machine import I2C, Pin, deepsleep
from sensors import sensors
from aes_tools import *
from lora_init import lora_init

ACK_wait_time = 2
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
# Initialize LoRa communication
lora = lora_init()

def onReceive(lora_modem,payload):
    #print("Waiting for LoRa packets...")
    if len(payload)==16:
        ack=aes_decrypt(payload,AES_KEY)
        rchan, cycle, delta, thold = ustruct.unpack('2i2f', ack)
        print("ACK:",rchan,cycle,delta,thold)   #, payload.decode())

# Function to send sensor data over LoRa
def send_lora_data(l, t, h):
    try:
        # Create the message with temperature, humidity, and luminosity
        message = f"L:{l:.2f},T:{t:.2f},H:{h:.2f}"
        print("Sending LoRa packet:", message)
        # prepare data packet with bytes
        data = ustruct.pack('i16s3f', 1254,'smartcomputerlab',l,t,h)
        enc_data=aes_encrypt(data,AES_KEY)
        # Convert message to bytes
        # lora.println(bytes(message, 'utf-8'))
        lora.println(enc_data)
        print("LoRa packet sent successfully.")
    except Exception as e:
        print("Failed to send LoRa packet:", e)

# Main program
                    # ACK waiting time depends on the protocol and data rate
def main():
    lora.onReceive(onReceive)
    lora.receive()
    while True:
        # Capture sensor data
        lumi, temp, humi = sensors(sda=8, scl=9)
        print("Luminosity:", lumi, "lux")
        print("Temperature:", temp, "C")
        print("Humidity:", humi, "%")
        # Send sensor data over LoRa
        send_lora_data(lumi, temp, humi)
        lora.receive()
        time.sleep(1)           # waiting for ACK frame
        lora.sleep()                      # only for deepsleep
        time.sleep(1)           # waiting for ACK frame
        deepsleep(10*1000)                # 10*1000 miliseconds
# Run the main program
main()

