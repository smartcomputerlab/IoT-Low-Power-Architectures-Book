import time

def sensors_display(sda, scl, luminosity, temperature, humidity, duration):
    # Initialize I2C bus
    i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=400000)
    # Adjust display width/height if different. Common sizes: 128x64 or 128x32.
    # Assuming a 128x64 display:
    width = 128
    height = 64
    # Initialize the OLED display
    oled = SSD1306_I2C(width, height, i2c)
    
    # Clear the display
    oled.fill(0)
    # Write text to display
    oled.text("Sensor readings", 0, 0)
    oled.text("Lux: {:.2f}".format(luminosity), 0, 16)
    oled.text("Temp: {:.2f}".format(temperature), 0, 32)
    oled.text("Humi: {:.2f}".format(humidity), 0, 48)
    # Update the display
    oled.show()
    if duration:
        time.sleep(duration)
        oled.poweroff()
        