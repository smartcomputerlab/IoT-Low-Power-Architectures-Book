import time
from machine import Pin
import neopixel

# LED ring setup
LED_PIN = 14  # Pin where the LED ring is connected
NUM_LEDS = 12
led_ring = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

def set_led_color(index, color):
    if 0 <= index < NUM_LEDS:
        led_ring[index] = color

def update_led_ring(hour, minute, second):
    led_ring.fill((0, 0, 0))  # Clear all LEDs
    # Map hour to red (0-11)
    hour_led = hour % 12
    set_led_color(hour_led, (255, 0, 0))
    # Map minute (in steps of 5) to green
    minute_led = minute // 5
    set_led_color(minute_led, (0, 255, 0))
    # Map second (in steps of 5) to blue
    second_led = second // 5
    set_led_color(second_led, (0, 0, 255))

    led_ring.write()

def main():
    while True:
        # Simulated time for demonstration purposes
        current_time = time.localtime()
        hour, minute, second = current_time[3], current_time[4], current_time[5]
        print(f"Time: {hour:02}:{minute:02}:{second:02}")
        update_led_ring(hour, minute, second)
        time.sleep(1)  # Update every second

if __name__ == "__main__":
    main()
    