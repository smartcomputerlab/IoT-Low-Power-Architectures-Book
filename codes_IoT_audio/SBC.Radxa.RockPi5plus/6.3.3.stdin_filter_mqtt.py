#!/usr/bin/python3
import sys,re
import paho.mqtt.client as mqtt
from whisper_filter import *
port = 1883
topic = "from/whisper"

def send_message(message):
    try:
        client = mqtt.Client()
        client.connect("broker.emqx.io",port,60)
        print("Publishing: "+message+" to topic: "+topic)
        client.publish(topic,message)
        client.disconnect()
        print("Message sent")
    except Exception as e:
        print("Failed to send. Error: {e}")

def main():
    try:
        while True:
            user_input = input("")
            result = whisper_filter(user_input)
            print(result)
            if result!=None:
                send_message(result)
                print("sent")
            else:
                print("not sent")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    