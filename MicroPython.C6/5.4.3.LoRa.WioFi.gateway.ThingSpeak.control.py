        message = {
            "luminosity": lumi,  "temperature": temp,  "humidity": humi }
        client.publish(topic, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")
        
    #client.disconnect()
# --- Receive LoRa Packet ---
def onReceive(lora_modem,payload):
    global chan; global wkey; global temp; global humi; global lumi; global start
    global cycle; global delta; global kpack
    if len(payload)==32:
        rssi = lora_modem.packetRssi()
        data=aes_decrypt(payload,AES_KEY)
        chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', data)
        print("Received LoRa packet:"+str(rssi))   #, payload.decode())
        cycle=random.randint(6,16)
        ack=ustruct.pack('2ifi',1234,cycle,delta,kpack)  	# chan,cycle,delta,kpack
        encrypted_ack=aes_encrypt(ack,AES_KEY)
        time.sleep(0.4)                         # wait short time before ack
        lora_modem.println(encrypted_ack)  # sending ACK packet
        print("ACK packet sent")
        sensor_display(temp,humi,lumi,rssi)
        if (time.time() - start) > 20:        # dynamic delay
            print("time to send")
            publish_sensor_data(MQTT_TOPIC_DATA, lumi, temp, humi)
            start = time.time()
            
    lora_modem.receive()

def main():
    global pack
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    client.set_callback(mqtt_callback)
    connect(SSID,PASS)
    print("Connected to MQTT broker.")
    client.connect()
    client.subscribe(MQTT_TOPIC_CONTROL)
    print("Subscribed to topic:", MQTT_TOPIC_CONTROL)
    time.sleep(0.4)
    while True:
        print("in the loop")
        client.wait_msg()
        time.sleep(2)

main()
