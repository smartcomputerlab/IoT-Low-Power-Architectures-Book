#./stream -m models/ggml-tiny.en.bin -c 1 -t 8 --step 2000 --length 8000 -kc -ac 1024  -vth 0.5 |\
# ./std_filter_mosquitto.py
#!/usr/bin/python3

import serial
import sys
import re
import paho.mqtt.client as mqtt

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


def filter_string(input_string):
    # patter to find
    pattern = bytes.fromhex("201b5b324b0d20").decode('latin1')
    start_index = input_string.rfind(pattern)
    if start_index == -1:
        return ""
    return input_string[start_index+7:]

def main():
    try:
        while True:
            # Read a string from standard input
            user_input = input("")
            #print(user_input)
            #print(user_input.encode('utf-8').hex())
            result = filter_string(user_input)
            print(result)
            #print(result.encode('utf-8').hex())
            if result.lower() == 'exit':
                print("Exiting program.")
                break
            if result[0:1]!="[" and result[0:1]!="(":               
            # Send the input to the serial port
                send_message(result)
                print("sent")
            else:
                print("not sent")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

