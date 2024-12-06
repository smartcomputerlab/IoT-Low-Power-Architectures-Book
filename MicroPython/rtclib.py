#rtclib.py
import machine
import esp32
from machine import Pin, RTC, deepsleep
import time
import ustruct
# Initialize RTC memory
rtc = RTC()

def init_data(s,c,d,k):
    init_data=ustruct.pack('f3i',s,d,c,k)
    rtc.memory(init_data)
    
def load_data():
    # Retrieve the counter value from RTC memory
    data = rtc.memory()
    sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    return sens,delta,cycle,kpack

def read_param():
    # Retrieve the counter value from RTC memory
    data = rtc.memory()
    if not data:
        sens = 20.0
        delta = 10
        cycle = 10
        kpack = 10
        init_data(sens,delta,cycle,kpack)
        return delta, cycle, kpack
    else:
        sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    return delta,cycle,kpack

# Function to increment the counter and save it in RTC memory
def save_data(pos, value):
    data = rtc.memory()
    sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    if pos==1:
        sens = value
    elif pos==2:
        delta = value
    elif pos==3:
        cycle = value
    elif pos==4:
        kpack = value
    else:
        print("error")
    new_data=ustruct.pack('f3i',sens,delta,cycle,kpack)
    rtc.memory(new_data)

def write_param(d,c,k):
    data = rtc.memory()
    sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    delta = d
    cycle = c
    kpack = k
    new_data=ustruct.pack('f3i',sens,delta,cycle,kpack)
    rtc.memory(new_data)

def write_sens(value):
    data=rtc.memory()
    sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    sens=value
    new_data=ustruct.pack('f3i',sens,delta,cycle,kpack)
    rtc.memory(new_data)

def read_sens():
    # Retrieve the counter value from RTC memory
    data = rtc.memory()
    if not data:
        sens = 20.0
        delta = 10
        cycle = 10
        kpack = 10
        init_data(sens,delta,cycle,kpack)
        return sens
    else:
        sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    return sens

def main():
    time.sleep(4)
    stored_temperature = read_sens()
    print(stored_temperature)
    stored_temperature = stored_temperature +0.1
    write_sens(stored_temperature)
    deepsleep(4000)
    
main()    
    
# init_data(20.0,100,10,12)
# delt,cycl,kpa=read_param()
# print("delta:",delt," cycle:",cycl," kpack:",kpa)
# write_sens(20.7)
# sens=read_sens()
# print("sensor:",sens)
