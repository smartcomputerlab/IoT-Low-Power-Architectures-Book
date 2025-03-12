from eeprom import EEPROM
from machine import I2C, Pin

# AT24C32 on 0x50
I2C_ADDR = 0x50     # DEC 80, HEX 0x50

i2c = I2C(0, scl=Pin(20), sda=Pin(19), freq=80000)
eeprom = EEPROM(addr=I2C_ADDR, at24x=32, i2c=i2c)

def just32(s):
    return "".join((s,'*'*(32 - len(s))))

def trim_string(data):
    return data.rstrip('*')  # Remove * from the end

def eeprom_write_prot_key(prot_key):
    eeprom.write(0, just32(prot_key))

def eeprom_read_prot_key():
    prot_key = eeprom.read(0,32)
    return trim_string(prot_key.decode())


def eeprom_write_ssid_pass(ssid,password):
    eeprom.write(32, just32(ssid))
    eeprom.write(64, just32(password))
    
def eeprom_read_ssid_pass():
    ssid = eeprom.read(32,32)
    password = eeprom.read(64,32)
    return trim_string(ssid.decode()), trim_string(password.decode())

def eeprom_write_channel_wkey(channel,wkey):
    eeprom.write(96, just32(str(channel)))
    eeprom.write(128, just32(wkey))

def eeprom_read_channel_wkey():
    channel = eeprom.read(96,32)
    wkey = eeprom.read(128,32)
    return int(trim_string(channel.decode())),trim_string(wkey.decode())

def eeprom_write_mqtt_server(server,topic):
    eeprom.write(160, just32(server))
    eeprom.write(192, just32(topic))

def eeprom_read_mqtt_server():
    server = eeprom.read(160,32)
    topic = eeprom.read(192,32)
    return trim_string(server.decode()),trim_string(topic.decode())

def eeprom_write_param(cycle,delta,kpack):
    eeprom.write(224, just32(str(cycle)))
    eeprom.write(256, just32(str(delta)))
    eeprom.write(288, just32(str(kpack)))

def eeprom_read_param():
    cycle = eeprom.read(224,32)
    delta = eeprom.read(256,32)
    kpack = eeprom.read(288,32)
    return int(trim_string(cycle.decode())),float(trim_string(delta.decode())),int(trim_string(kpack.decode()))

# get LCD infos/properties
print("EEPROM is on I2C address 0x{0:02x}".format(eeprom.addr))
print("EEPROM has {} pages of {} bytes".format(eeprom.pages, eeprom.bpp))
print("EEPROM size is {} bytes ".format(eeprom.capacity))

eeprom_write_prot_key("0123456789abcdef")
pk = eeprom_read_prot_key()
print(pk)

eeprom_write_ssid_pass("PhoneAP","smartcomputerlab")
s,p = eeprom_read_ssid_pass()
print(s,p)

eeprom_write_channel_wkey(123456,"YOX31M0EDKO0JATK")
c,k = eeprom_read_channel_wkey()
print(c,k)

eeprom_write_mqtt_server("broker.emqx.io","allmysensors")
se,to = eeprom_read_mqtt_server()
print(se,to)

eeprom_write_param(12,0.01,10)
cy,de,kp = eeprom_read_param()
print(cy,de,kp)




