from machine import Pin, I2C
import ubinascii
import machine
from wifi_tools import *
from sensors import sensors
import time
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = 'PhoneAP'
PASSWORD = 'smartcomputerlab'
# MQTT broker details
MQTT_BROKER = 'broker.emqx.io'  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID !!!
MQTT_TOPIC = 'esp32/sensor_data'  # Replace with your topic

# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
print(MQTT_CLIENT_ID)
def connect_mqtt():
    """Connect to the MQTT broker."""
    try:
        client.connect()
        print("Connected to MQTT broker.")
    except Exception as e:
        print("Failed to connect to MQTT broker:", e)

def disconnect_mqtt():
    """Disconnect from the MQTT broker."""
    client.disconnect()
    print("Disconnected from MQTT broker.")

def publish_sensor_data():
    """Publish sensor data to MQTT broker."""
    luminosity, temperature, humidity = sensors(sda=19, scl=20)
    
    if luminosity is not None and temperature is not None and humidity is not None:
        message = {
            "luminosity": luminosity,  "temperature": temperature, "humidity": humidity }
        client.publish(MQTT_TOPIC, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")

def main():
    # Initialize WiFi and connect to access point
    connect_wifi(SSID, PASSWORD)
    # Connect to MQTT
    connect_mqtt()
    try:
        # Publish sensor data every 10 seconds
        while True:
            publish_sensor_data()
            time.sleep(10)
    finally:
        # Disconnect from MQTT and WiFi on exit
        disconnect_mqtt()
        #disconnect_wifi()

# Run the main function
main()
