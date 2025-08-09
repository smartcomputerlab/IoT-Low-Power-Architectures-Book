from sensors_display import sensors_display

# Example sensor values
lumi = 123.4567
temp = 25.6789
humi = 45.2345
# Call the function with GPIO pin numbers for SDA and SCL
# Adjust SDA, SCL pins according to your board wiring
sensors_display(8, 9, lumi, temp, humi, 0)

