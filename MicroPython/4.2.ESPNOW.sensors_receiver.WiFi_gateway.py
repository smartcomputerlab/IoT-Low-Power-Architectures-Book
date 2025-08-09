import network, time, espnow, ustruct, urequests
from machine import Pin

def wifi_reset():   # Reset wifi to AP_IF off, STA_IF on and disconnected
  sta = network.WLAN(network.STA_IF); sta.active(False)
  ap = network.WLAN(network.AP_IF); ap.active(False)
  sta.active(True)
  sta.config(txpower=5.0)
  while not sta.active():
      time.sleep(0.1)
  sta.disconnect()   # For ESP8266
  while sta.isconnected():
      time.sleep(0.1)
  return sta, ap

# ThingSpeak API details
# THINGSPEAK_WRITE_API_KEY = 'YOX31M0EDKO0JATK' - this key is sent by the terminal
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Function to send data to ThingSpeak
def send_data_to_thingspeak(wkey, lumi, temp, humi):
    try:
        # very useful line !
        url = f"{THINGSPEAK_URL}?api_key={wkey}&field1={lumi}&field2={temp}&field3={humi}"
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi)
    except Exception as e:
        print("Failed to send data:", e)

sta, ap = wifi_reset()  # Reset wifi to AP off, STA on and disconnected

sta.connect('Bbox-9ECEBF79', '54347A3EA6A1D6C36EF6A9E5156F7D')
while not sta.isconnected():  # Wait until connected...
    time.sleep(0.1)
sta.config(pm=sta.PM_NONE)  # ..then disable power saving
print(sta.ifconfig())

# Print the wifi channel used AFTER finished connecting to access point
print("Proxy running on channel:", sta.config("channel"))
e = espnow.ESPNow(); e.active(True)
for peer, msg in e:
        while True:
            host, data = e.recv()
            if data:
                chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', data)   # wkey may be topic
                print(host)
                for_wkey="{:s}".format(wkey)
                print("wkey:"+str(for_wkey)+" lumi:"+str(lumi)+" temp:"+str(temp)+" humi:"+str(humi))
                msg= "lumi:"+str(lumi)+"; temp:"+str(temp)+"; humi:"+str(humi)
                # Send data to ThingSpeak
                send_data_to_thingspeak(for_wkey,lumi, temp, humi)

