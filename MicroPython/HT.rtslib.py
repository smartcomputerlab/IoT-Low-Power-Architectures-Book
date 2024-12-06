#rtclib.py
import machine
import esp32
from machine import Pin, RTC, deepsleep
import time
import ustruct
# Initialize RTC memory
rtc = RTC()

def init_data():
    sens = 10.0
    delta = 10		# to modify by 0.01 factor: 10*0.01 = 0.1°C
    cycle = 10      #  to mopdify by 1000 factor: 10000 ms in deepsleep()
    kpack = 10      # once every 10 cycles
    init_data=ustruct.pack('f3i',sens,delta,cycle,kpack)
    rtc.memory(init_data)
    return sens,delta,cycle,kpack

def read_sens():
    # Retrieve the counter value from RTC memory
    data = rtc.memory()
    if not data:
        sens,delta,cycle,kpack =init_data()
        return sens
    else:
        sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    return sens

def read_param():
    # Retrieve the counter value from RTC memory
    data = rtc.memory()
    if not data:
        sens,delta,cycle,kpack =init_data()
        return delta,cycle,kpack
    else:
        sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    return delta,cycle,kpack

def write_sens(value):
    data=rtc.memory()
    if not data:
        sens,delta,cycle,kpack =init_data()
    else:
        sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
    
    sens=value
    new_data=ustruct.pack('f3i',sens,delta,cycle,kpack)
    rtc.memory(new_data)

def write_param(d,c,k):
    data = rtc.memory()
    if not data:
        sens,delta,cycle,kpack =init_data()
    else:
        sens,delta,cycle,kpack=ustruct.unpack('f3i',data)
        
    delta = d
    cycle = c
    kpack = k
    new_data=ustruct.pack('f3i',sens,delta,cycle,kpack)
    rtc.memory(new_data)



# The following code may be uncommented for test
# def main():
#     time.sleep(4)
#     print("param")
#     sdelta,scycle,skpack = read_param()
#     print(sdelta, scycle, skpack)
#     sdelta = sdelta + 1
#     write_param(sdelta,scycle,skpack)
#     print("sensor")
#     stored_temperature = read_sens()
#     print(stored_temperature)
#     stored_temperature = stored_temperature + 0.1
#     write_sens(stored_temperature)
#     
#     deepsleep(4000)
#     
# main()    
    
