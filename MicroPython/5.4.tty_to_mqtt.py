import network
import machine
import time
from umqtt.simple import MQTTClient
from machine import UART

# WiFi Configuration
SSID = "PhoneAP"
PASSWORD = "smartcomputerlab"
# MQTT Configuration
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "esp/uart"
# UART Configuration
UART_BAUDRATE = 9600
uart = UART(2, baudrate=UART_BAUDRATE, tx=17, rx=16)

# Connect to WiFi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(txpower=8.5)  # Set WiFi transmission power to 8.5 dBm
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print("Waiting for connection...")

    print("WiFi connected!", wlan.ifconfig())

# Send message to MQTT
def send_to_mqtt(message):
    try:
        client = MQTTClient("esp32", MQTT_BROKER)
        client.connect()
        client.publish(MQTT_TOPIC, message)
        print(f"Sent to MQTT: {message}")
        client.disconnect()
    except Exception as e:
        print("Failed to send to MQTT:", e)

# Main execution
connect_to_wifi()

print("Ready to receive UART messages and send to MQTT...")
while True:
    if uart.any():
        time.sleep(0.1)# necessary to synchronize the UART input buffer
        message = uart.readline().decode('utf-8').strip()
        if message:
            print(f"Received from UART: {message}")
            send_to_mqtt(message)
            