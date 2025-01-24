from machine import UART, Pin
import utime

# Initialize UART interface
uart = UART(1, baudrate=9600, tx=Pin(16), rx=Pin(17))  # TX on GPIO1, RX on GPIO0

# Initialize lite UART interface
# uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))  # TX on GPIO1, RX on GPIO0

print("UART Test Program")

# Test data to send
test_data = "Hello, UART interface on our DevKit"

try:
    # Send data over UART
    print("Sending data: ", test_data)
    uart.write(test_data)

    # Small delay to ensure the data is transmitted
    utime.sleep(1)

    # Read data from UART
    if uart.any():
        received_data = uart.read()
        print("Received data: ", received_data.decode('utf-8'))
    else:
        print("No data received.")

except Exception as e:
    print("An error occurred:", e)

finally:
    print("Program completed.")
    