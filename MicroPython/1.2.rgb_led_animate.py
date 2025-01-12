import time
from machine import Pin
import neopixel

# Configuration
LED_COUNT = 12  # Number of LEDs in the ring
PIN_NUM = 3     # Pin connected to the LED ring (GPIO2 in this case)

# Initialize the NeoPixel ring
np = neopixel.NeoPixel(Pin(PIN_NUM), LED_COUNT)

def clear_ring():
    """Turn off all LEDs."""
    for i in range(LED_COUNT):
        np[i] = (0, 0, 0)
    np.write()

def color_wheel(pos):
    """Generate RGB color based on a position (0-255)."""
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def animate_ring():
    """Animate the RGB ring with a color wheel effect."""
    position = 0  # Start position on the color wheel
    try:
        while True:
            for i in range(LED_COUNT):
                # Calculate the color for each LED based on the wheel position
                pixel_index = (position + (i * 256 // LED_COUNT)) % 256
                np[i] = color_wheel(pixel_index)
            np.write()
            position = (position + 1) % 256  # Move the position
            time.sleep(0.05)  # Delay to control animation speed

    except KeyboardInterrupt:
        clear_ring()
        print("Animation stopped.")

if __name__ == "__main__":
    print("Starting RGB ring animation...")
    animate_ring()
    