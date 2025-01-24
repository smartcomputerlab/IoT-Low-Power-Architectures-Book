#!/usr/bin/python3
from piper_play import *
import paho.mqtt.client as mqtt
BROKER_ADDRESS = "broker.emqx.io"
BROKER_PORT = 1883
TOPIC = "from/whisper"  # Replace with your desired topic
# Callback function for when a message is received
def on_message(client, userdata, msg):
    voix = "female"
    try:
        msg = msg.payload.decode("utf-8").strip()
        msg = msg + "\n"
        print(f"Received message: {msg}")
        piper_play(msg,voix)

    except Exception as e:
        print(f"Error handling message: {e}")

# Function to subscribe to the MQTT topic
def subscribe_to_topic():
    try:
        client = mqtt.Client()
        client.on_message = on_message
        print(f"Connecting to MQTT broker at {BROKER_ADDRESS}:{BROKER_PORT}...")
        client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
        print(f"Subscribing to topic: {TOPIC}")
        client.subscribe(TOPIC)
        print("Listening for messages...")
        client.loop_forever()

    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

def main():
    subscribe_to_topic()

main()
