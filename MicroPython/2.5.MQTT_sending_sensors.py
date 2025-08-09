from machine import Pin, I2C
import ubinascii
import machine
from wifi_tools import *
from sensors import *
import time
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'
# MQTT broker details
MQTT_BROKER = "broker.emqx.io"  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID
MQTT_TOPIC = 'risc-v/sensor_data'  # Replace with your topic
# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

def connect_mqtt():
    """Connect to the MQTT broker."""
    try:
        client.connect()
        print("Connected to MQTT broker.")
    except Exception as e:
        print("Failed to connect to MQTT broker:", e)

def disconnect_mqtt():
    client.disconnect()
    print("Disconnected from MQTT broker.")

def publish_sensor_data():
    """Publish sensor data to MQTT broker."""
    luminosity, temperature, humidity = sensors(sda=8, scl=9)
    
    if luminosity is not None and temperature is not None and humidity is not None:
        message = {
            "f3": humidity,
            "f2": temperature,
            "f1": luminosity
        }
        client.publish(MQTT_TOPIC, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")
        
        # Main function
def main():
    # Initialize WiFi and connect to access point
    res=connect_WiFi(SSID, PASSWORD)
    if res==True:
        print("WiFi connected")
    time.sleep(1)
    connect_mqtt()
    try:
        # Publish sensor data every 10 seconds
        while True:
            publish_sensor_data()
            time.sleep(10)
    finally:
        # Disconnect from MQTT and WiFi on exit
        disconnect_mqtt()
        time.sleep(1)
        disconnect_WiFi()

# Run the main function
main()

