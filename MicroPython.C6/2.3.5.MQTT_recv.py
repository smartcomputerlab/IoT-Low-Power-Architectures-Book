from machine import Pin, I2C
from wifi_tools import *
from umqtt.simple import MQTTClient
from ssd1306 import SSD1306_I2C
from time import sleep_ms
# WiFi credentials
SSID = 'PhoneAP'
PASS = 'smartcomputerlab'
# MQTT broker details
MQTT_BROKER = 'broker.emqx.io'
MQTT_PORT = 1883
MQTT_TOPIC = b'sensor/readings'  # Topic as bytes
# Initialize I2C and SSD1306 OLED display (SDA=Pin 8, SCL=Pin 9)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Function to display messages on the OLED
def display_message(message):
    oled.fill(0)  # Clear display
    oled.text("MQTT Message:", 0, 0)
    oled.text(message, 0, 20)
    oled.show()

# MQTT message callback function
def mqtt_callback(topic, msg):
    print("Received message:", msg)
    display_message(msg.decode())  # Display message on OLED
    

# Initialize WiFi and connect to access point
connect_wifi(SSID,PASS)

# Initialize MQTT client
client = MQTTClient('esp32_client', MQTT_BROKER, port=MQTT_PORT)

try:
    # Connect to MQTT broker
    client.set_callback(mqtt_callback)
    client.connect()
    print("Connected to MQTT broker.")
    # Subscribe to the topic
    client.subscribe(MQTT_TOPIC)
    print("Subscribed to topic:", MQTT_TOPIC)
    
    # Main loop to check for messages
    while True:
        # Wait for incoming messages
        client.wait_msg()
        # Short delay between checks to avoid high CPU usage
        sleep_ms(500)
except Exception as e:
    print("Error:", e)
finally:
    # Disconnect from MQTT broker and WiFi
    client.disconnect()
    disconnect_wifi()
    print("Disconnected from MQTT broker and WiFi.")
    