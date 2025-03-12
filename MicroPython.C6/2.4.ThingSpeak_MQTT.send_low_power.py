from machine import Pin, I2C, deepsleep
import ubinascii, urequests
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
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID
MQTT_TOPIC = 'esp32/sensor_data'  # Replace with your topic
led=Pin(15,Pin.OUT)
# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
rtc = machine.RTC()
def publish_sensor_data(lumi, temp, humi):
    """Publish sensor data to MQTT broker."""
    client.connect()
    time.sleep(1)
    if lumi is not None and temp is not None and humi is not None:
        message = {"luminosity": lumi,"temperature": temp,"humidity": humi }
        client.publish(MQTT_TOPIC, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")
    client.connect()
    client.disconnect()
 
# Function to send data to ThingSpeak
def send_data_to_thingspeak(lumi, temp, humi):
    try:
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi)
        #url = "http://2.12.92.92:443/update?key=HEU64K3PGNWG36C4"+sf1+sf2+sf3
        url = "https://107.23.148.232/update?key=YOX31M0EDKO0JATK"+sf1+sf2+sf3
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi)
    except Exception as e:
        print("Failed to send data:", e)

def main():
    delta=0.1
    led.value(0)
    # Retrieve cycle counter from RTC memory
    rtc_mem = rtc.memory()
    if len(rtc_mem) == 0:
        stemp = 20.0
    else:
        stemp = float(rtc_mem.decode())
        
    luminosity, temperature, humidity = sensors(sda=19, scl=20)
    if (abs(stemp-temperature)> delta):
        led.value(1)
        rtc.memory(str(temperature).encode())
        # Initialize WiFi and connect to access point
        connect_wifi(SSID, PASSWORD)
        print("WiFi connected")
        publish_sensor_data(luminosity, temperature, humidity)
        send_data_to_thingspeak(luminosity, temperature, humidity)
        time.sleep(1)
        disconnect()
        led.value(0)
        
    deepsleep(15*1000)
    
# Run the main function
main()
