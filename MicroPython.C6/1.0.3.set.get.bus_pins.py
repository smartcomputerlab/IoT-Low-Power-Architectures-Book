# Get and print I2C, SPI, and UART pin configurations
import machine
import esp32

# Set and get I2C, SPI, and UART pin configurations for ESP32C6
def set_get_bus_pins():
    # Define pins for ESP32C6
    i2c = machine.I2C(0, scl=machine.Pin(20), sda=machine.Pin(19))
    spi = machine.SPI(1, sck=machine.Pin(23), mosi=machine.Pin(22), miso=machine.Pin(21))
    uart = machine.UART(1, tx=machine.Pin(17), rx=machine.Pin(16))
    
    print("I2C Pins: SCL =", str(i2c)) # 
    print("SPI Pins: SCK =", str(spi)) #  
    print("UART Pins: TX =", str(uart)) #  

set_get_bus_pins()
