import time, ustruct, ubinascii, urequests
from machine import I2C, Pin, freq, deepsleep
from sensors import sensors
from wifi_tools import *
from rtc_tools import *
from nvs_tools import *
SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'
nvs_key="param"                            # key to NVS records
led = Pin(3, Pin.OUT)  
        
def send_wifi_data(wkey,lumi,temp,humi):
    connect_WiFi(SSID, PASSWORD)
    print("WiFi connected")
    try:
        swkey=wkey.decode()+"\0"               # adding ASCI zero to decoded bytes
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi)
        url = "https://thingspeak.com/update?key="+swkey+sf1+sf2+sf3
        #url = "https://api.thingspeak.com/update?key="+"YOX31M0EDKO0JATK"+sf1+sf2+sf3
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi)
    except Exception as e:
        print("Failed to send packet:", e)

def main():
    global cdef; global ts_chan; global ncycle
    #freq(20000000)
    print("Reading ts from internal EEPROM...")
    len,ts_rparam = read_nvs_ts(nvs_key)
    if len:
        ts_chan,ts_wkey=ustruct.unpack("i16s",ts_rparam)
        print("len:",len,"ts_chan:",ts_chan,"ts_wkey:",ts_wkey.decode())
    print("Reading pow from internal EEPROM...")
    len,pow_rparam = read_nvs_power(nvs_key)
    if len:
        cdef,cmax,dmin,dmax,tlow,thigh=ustruct.unpack("2i4f",pow_rparam)
        print("len:",len,", cdef:",cdef,", cmax:",cmax,", dmin:",dmin,", dmax:",dmax,", tlow:",tlow,", thigh:",thigh)    
        
    while True:
        ncycle,npos,nneg= rtc_load_param()
        ssens= rtc_load_sensor(); sdelta= rtc_load_delta()
        print("ncycle:" +str(ncycle));
        lumi, temp, humi = sensors(sda=8, scl=9)
        print("Luminosity:", lumi, "lux")
        print("Temperature:", temp, "C")
        print("Humidity:", humi, "%")
        print("current: "+str(temp)+" saved: "+str(ssens));   # sensor is temperature
        print(dmin,dmax,sdelta);
        print("thigh:",thigh);print("tlow:",tlow);print("temp:",temp)
        if temp>thigh or temp<tlow :              # testing thresholds - urgent packet
            print("send urgent packet");  led.on()
            ncycle=1; npos=0; nneg=0; rtc_store_param(ncycle,npos,nneg)  # back to 1 cycle
            sdelta = dmin; rtc_store_delta(sdelta)
            send_wifi_data(ts_wkey,lumi, temp, humi)
            
        elif abs(ssens-temp)>sdelta or (thigh-temp)<sdelta or (temp-tlow)<sdelta: # delta
            print("send normal packet")
            rtc_store_sensor(temp) ; led.on()
            if npos :
                if ncycle > 2:
                    ncycle= int(ncycle/2)
                else:
                    if sdelta< dmax:
                        sdelta = sdelta+0.1*sdelta         # new delta
                        rtc_store_delta(sdelta)      
            npos=npos+1; nneg=0  # positive and negative counters
            rtc_store_param(ncycle,npos,nneg)
            send_wifi_data(ts_wkey,lumi, temp, humi)
            led.off()
        else:
            print("data packet NOT sent")
            if nneg :
                if ncycle < cmax:
                    ncycle = int(ncycle*2)           # maximum factor 64 (64*15sec)
                else :
                    if sdelta> dmin:
                        sdelta = sdelta-0.1*sdelta
                        rtc_store_delta(sdelta)
            npos=0; nneg=nneg+1
            rtc_store_param(ncycle,npos,nneg)
        time.sleep(0.1)
        print("new_cycle",ncycle*cdef)
        print("new_delta",sdelta)
        deepsleep(ncycle*cdef*1000)                # 10*1000 miliseconds
# Run the main program
main()

