# rtc_tools.py
import machine
import ustruct

rtc = machine.RTC()

# Function to store four integer/float values in RTC memory
def rtc_store_param(cycle, pos, neg):  # these values define next cycle length factor
    data = rtc.memory()
    c,p,n,s,d = ustruct.unpack('3i2f', data);
    data = ustruct.pack('3i2f',cycle,pos,neg,s,d)
    rtc.memory(data)

def rtc_load_param():
    # Retrieve the packed data from RTC memory
    c=1; p=0; n=0; s=20.0; d=0.1
    data = rtc.memory()
    if not data:
        data = ustruct.pack('3i2f',c,p,n,s,d)
        rtc.memory(data)
    # Unpack the integers from the byte array
    c,p,n,s,d = ustruct.unpack('3i2f', data);
    return c, p, n

def rtc_store_delta(delta):	    # stores last sent sensor and delta values
    data = rtc.memory()
    c,p,n,s,d = ustruct.unpack('3i2f', data);
    data = ustruct.pack('3i2f',c,p,n,s,delta)
    rtc.memory(data)
    
def rtc_load_delta():                  # loads stored sensor and delta values, or default init
    c=0; p=0; n=0; s=20.0; d=0.1
    data = rtc.memory()
    if not data:
        data = ustruct.pack('3i2f',c,p,n,s,d)
        rtc.memory(data)
    c,p,n,s,d = ustruct.unpack('3i2f', data);
    return d

def rtc_store_sensor(sensor):	    # stores last sent sensor and delta values
    data = rtc.memory()
    c,p,n,s,d = ustruct.unpack('3i2f', data);
    data = ustruct.pack('3i2f',c,p,n,sensor,d)
    rtc.memory(data)
    
def rtc_load_sensor():                  # loads stored sensor and delta values, or default init
    c=0; p=0; n=0; s=20.0; d=0.1
    data = rtc.memory()
    if not data:
        data = ustruct.pack('3i2f',c,p,n,s,d)
        rtc.memory(data)
    c,p,n,s,d = ustruct.unpack('3i2f', data);
    return s

