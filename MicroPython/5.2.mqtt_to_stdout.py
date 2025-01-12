#./mqtt_to_stdout.py | ./piper -m models/GB/female.onnx --output-raw | _
# aplay -r 16000 -f S16_LE -t raw -
#!/usr/bin/python3
import serial, tempfile, os
import paho.mqtt.client as mqtt
import subprocess
BROKER_ADDRESS = "broker.emqx.io"
BROKER_PORT = 1883
TOPIC = "from/whisper"  # Replace with your desired topic

# Callback function for when a message is received
def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode("utf-8").strip()
        message = message + "\n"
        print(f"Received message: {message}")
        with tempfile.NamedTemporaryFile(delete=False, mode='w',prefix='mqtt_', suffix='.txt') as temp_file:
            temp_file.write(message)
            print(f"Message written to temporary file: {temp_file}")
            # Read back from the temporary file and use echo command
        with open(temp_file.name, 'r') as file:
            file_content = file.read()
            print(f"Read from temporary file: {file_content}")
            os.remove(temp_file.name)
            os.system(f'echo "{file_content}"')

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
