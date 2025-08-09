import time, ustruct
from machine import I2C, Pin, freq, deepsleep
from sensors import sensors
from lora_init import lora_init
from rtc_tools import *
from nvs_tools import *
from aes_tools import *
# Initialize LoRa communication
lora = lora_init()
aes_key="smartcomputerlab"     # constant - 1 ECB mode
cdef=1; ts_chan=1234; ncycle=1
ACK_wait_time = 2                     # ACK waiting time depends on the protocol and data rate
nvs_key="param"
led = Pin(3, Pin.OUT)

def onReceive(lora_modem,payload):
    global cdef; global ncycle
    if len(payload)==16:                  # the payload: max_cycle, t_high, t_low
        ack=aes_decrypt(payload,aes_key)
        chan,cntr,c_par,d_par=ustruct.unpack('3if',ack)   # ack parameters - to confirm
        if chan==ts_chan:
            print("short ACK received")             # no channel test
        lora.sleep()                      # only for deepsleep
        time.sleep(0.1)
        deepsleep(ncycle*cdef*1000)
        
    if len(payload)==32:                  # the payload: max_cycle, t_high, t_low
        ack=aes_decrypt(payload,aes_key)
        chan,cntr,c_def,c_max,d_min,d_max,t_low,t_high=ustruct.unpack("4i4f",ack) 
        if chan==ts_chan:
            print("long ACK parameters received")             # no channel test
            value=ustruct.pack("2i4f",c_def,c_max,d_min,d_max,t_low,t_high)
            write_nvs_power(nvs_key, value)
            print("new parameters written to nvs")
        lora.sleep()                      # only for deepsleep
        time.sleep(0.1)
        ncycle,npos,nneg=rtc_load_param()
        print(ncycle*cdef)
        deepsleep(ncycle*cdef*1000)   
        
def send_lora_data(ts_chan,ts_wkey,l,t,h):
    try:
        message = f"L:{l:.2f},T:{t:.2f},H:{h:.2f}"
        print("Sending LoRa packet:", message)
        data = ustruct.pack('i16s3f',ts_chan,ts_wkey,l,t,h)  # 32 bytes - short version
        enc_data=aes_encrypt(data,aes_key)
        lora.println(enc_data)
        print("LoRa encrypted packet sent successfully.")
    except Exception as e:
        print("Failed to send LoRa packet:", e)

def main():
    global cdef; global ts_chan; global ncycle
    freq(20000000)
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
        
    lora.onReceive(onReceive)
    lora.receive()
    while True:
        ncycle,npos,nneg= rtc_load_param()
        ssens= rtc_load_sensor(); sdelta= rtc_load_delta()
        print("ncycle:" +str(ncycle));
        lumi, temp, humi = sensors(sda=8, scl=9)
        print("Luminosity:", lumi, "lux")
        print("Temperature:", temp, "C")
        print("Humidity:", humi, "%")
        print("current: "+str(temp)+" saved: "+str(ssens));  # sensor is temperature
        print(dmin,dmax,sdelta);
        if temp>thigh or temp<tlow :              # testing thresholds - urgent packet
            print("send urgent packet");  led.on()
            ncycle=1; npos=0; nneg=0; rtc_store_param(ncycle,npos,nneg)  # back to 1 cycle
            sdelta = dmin; rtc_store_delta(sdelta)
            send_lora_data(ts_chan,ts_wkey,lumi, temp, humi)
            lora.receive()
            time.sleep(ACK_wait_time)
            print("data packet sent, no ack received")
            send_lora_data(ts_chan,ts_wkey,lumi, temp, humi)
            lora.receive()
            time.sleep(ACK_wait_time)
            print("data packet re-sent, no ack received")
            led.off()
            
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
            send_lora_data(ts_chan,ts_wkey,lumi, temp, humi)
            lora.receive()
            time.sleep(ACK_wait_time)
            print("data packet sent, no ack received")
            send_lora_data(ts_chan,ts_wkey,lumi, temp, humi)
            lora.receive()
            time.sleep(ACK_wait_time)
            print("data packet re-sent, no ack received")
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
            # waiting for ACK frame
        lora.sleep()                      # only for deepsleep
        time.sleep(0.1)
        print(ncycle*cdef)
        print(sdelta)
        deepsleep(ncycle*cdef*1000)                # 10*1000 miliseconds
# Run the main program
main()

