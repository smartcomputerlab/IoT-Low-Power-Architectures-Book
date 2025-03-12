from machine import SoftI2C, Pin
import ssd1306  # Ensure SSD1306 OLED display driver is installed
import time

i2c = SoftI2C(scl=Pin(20), sda=Pin(19), freq=400000)  # I2C on SCL=9 and SDA=8 with 400 kHz
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
def sensor_display(temp,humi,lumi,rssi,duration):
    for_temp="{:.2f}".format(temp);for_humi="{:.2f}".format(humi);for_lumi="{:.2f}".format(lumi);
    oled.fill(0)  # Clear the display
    oled.text("LoRa Packet:", 0, 0)
    oled.text("T: "+for_temp, 0, 12)
    oled.text("H: "+for_humi, 0, 24)
    oled.text("L: "+for_lumi, 0, 36)
    oled.text("RSSI: "+str(rssi), 0, 48)
    oled.show()
    if duration:
        time.sleep(duration)
        oled.poweroff()

