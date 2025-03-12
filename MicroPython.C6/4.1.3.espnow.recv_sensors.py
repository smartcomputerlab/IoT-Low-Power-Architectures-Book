import network, ustruct
import espnow

# Initialize WiFi in station mode (without connecting to AP)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()  # Disconnect from any AP

# Initialize ESPNOW
esp = espnow.ESPNow()
esp.active(True)

# Add a peer (MAC address will be learned dynamically)
# ESPNOW requires at least one peer to be added before receiving data
esp.add_peer(b'\xff' * 6)  # Broadcast address to receive from any device

print("ESP32 ESPNOW Receiver Initialized. Waiting for data...")
e = espnow.ESPNow(); e.active(True)
for peer, msg in e:
    while True:
        host, data = e.recv()
        if data:
            chan,wkey,bat,lumi,temp,humi,s4,s5,s6 = ustruct.unpack('i16s7f',data) 
            print(host)
            for_wkey="{:s}".format(wkey)
            print("wkey:"+str(for_wkey)+" lumi:"+str(lumi)+" temp:"+str(temp)+" humi:"+str(humi))
            msg= "lumi:"+str(lumi)+"; temp:"+str(temp)+"; humi:"+str(humi)
            