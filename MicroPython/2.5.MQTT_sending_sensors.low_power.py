from machine import Pin, I2C, deepsleep
import ubinascii
import machine
from wifi_tools import *
from sensors import sensors
import time
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'
# MQTT broker details
MQTT_BROKER = 'broker.emqx.io'  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID
MQTT_TOPIC = 'esp32/sensor_data'  # Replace with your topic
# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
rtc = machine.RTC()

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

def publish_sensor_data(luminosity, temperature, humidity):
    """Publish sensor data to MQTT broker."""
    if luminosity is not None and temperature is not None and humidity is not None:
        message = {
            "luminosity": luminosity,"temperature": temperature,"humidity": humidity
        }
        client.publish(MQTT_TOPIC, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")
# Main function
def main():
    delta=0.1
    # Retrieve cycle counter from RTC memory
    rtc_mem = rtc.memory()
    if len(rtc_mem) == 0:
        stemp = 20.0
    else:
        stemp = float(rtc_mem.decode())
    luminosity, temperature, humidity = sensors(sda=8, scl=9)
    if (abs(stemp-temperature)> delta):
        rtc.memory(str(temperature).encode())
        connect_WiFi(SSID, PASSWORD)
        connect_mqtt()          # Connect to MQTT
        time.sleep(1)
        publish_sensor_data(luminosity, temperature, humidity)
        time.sleep(1)
        disconnect_mqtt() # Disconnect from MQTT and WiFi on exit
        time.sleep(1)
        disconnect_WiFi()
        print("message sent")
    else:
        print("message not sent")
    deepsleep(10*1000)
    
main()

