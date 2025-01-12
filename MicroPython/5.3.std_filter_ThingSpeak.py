#./stream -m models/ggml-tiny.en.bin -c 1 -t 8 --step 2000 --length 8000 -kc -ac 1024  -vth 0.5 |\
#./std_filter_thingspeak.py
#!/usr/bin/python3

import serial
import sys
import re
import requests
THINGSPEAK_API_URL="https://api.thingspeak.com/update"
CHANNEL_API_KEY= "4K897XNNHTW7I4NO"
FIELD_NUMBER = 1

def send_to_thingspeak(message):
    try:
        # prepare payload
        payload = {
                f"field{FIELD_NUMBER}": message,
                "api_key": CHANNEL_API_KEY
                }

        print(f"Sending message: '{message}' to ThingSpeak on field {FIELD_NUMBER}..")
        response = requests.post(THINGSPEAK_API_URL, data=payload)

        if response.status_code == 200:
            print("Message sent to TS")
        else:
            print("Failed to send to TS")

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
                    send_to_thingspeak(result)
                    print("sent")
                else:
                    print("not sent")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    