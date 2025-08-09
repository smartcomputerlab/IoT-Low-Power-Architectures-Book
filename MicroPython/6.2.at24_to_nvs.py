from nvs_tools import *
from at24_tools import *
from check_at24 import *

def at24_to_nvs():
    nvs_key = "param" 
    if check_eeprom():
        I2C_SCL = 9; I2C_SDA = 8
        i2c = machine.I2C(0, scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA))
        eeprom = AT24C32(i2c)
        ts_addr = 0x00  # Starting address in EEPROM for ThingSpeak meta-parameters
        pow_addr = 0x80   # 255 - starting address for power mata-parameters
        print("Reading from AT24C32...")
        ts_rparam = eeprom.read_at24(ts_addr, 20)    # len ts_rparam 
        pow_rparam = eeprom.read_at24(pow_addr, 24)  # len pow_rparam
        print("Writing to NVS...")
        write_nvs_ts(nvs_key, ts_rparam)
        write_nvs_power(nvs_key, pow_rparam)
    else:
        print("no AT24CXX module found..")
    print("Reading from NVS...")
    len,ts_rparam = read_nvs_ts(nvs_key)
    if len:
        chan,wkey=ustruct.unpack("i16s",ts_rparam)
        print("len:",len,"ts_chan:",chan,"ts_wkey:",wkey.decode())
    len,pow_rparam = read_nvs_power(nvs_key)
    if len:
        cdef,cmax,dmin,dmax,tlow,thigh=ustruct.unpack("2i4f",pow_rparam)
        print("len:",len,", cdef:",cdef,", cmax:",cmax,", dmin:",dmin,", dmax:",dmax,", tlow:",tlow,", thigh:",thigh)

