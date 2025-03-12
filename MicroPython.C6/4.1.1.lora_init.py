#lora_init.py

from machine import Pin, SPI
import time
import sx127x  # SX127x LoRa driver (ensure the library is installed)
import esp32

# --- LoRa Pins and SPI Bus Setup --- BF2
lora_pins = {
    'dio_0': 3,        # DIO0 pin for interrupt
    'ss': 1,           # Slave Select (SS)
    'reset': 14,       # Reset pin
    'sck': 23,          # SPI Clock pin
    'miso': 21,         # SPI MISO pin
    'mosi': 22          # SPI MOSI pin
}

# SPI bus configuration for SX1276
lora_spi = SPI(
    baudrate=10000000,    # Set baudrate to 10 MHz
    polarity=0,           # Clock polarity (CPOL)
    phase=0,              # Clock phase (CPHA)
    bits=8,               # 8 bits per transfer
    firstbit=SPI.MSB,     # MSB first
    sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),   # SCK (clock)
    mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),   # MOSI (Master Out Slave In)
    miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP),    # MISO (Master In Slave Out)
)

# LoRa configuration with default parameters
lora_default = {
    'frequency': 868E6,             # Frequency for Europe (868 MHz ISM band)
    'tx_power_level': 14,           # Transmission power level (14 dBm)
    'signal_bandwidth': 125E3,      # Signal bandwidth (125 kHz)
    'spreading_factor': 7,          # Spreading factor (7)
    'coding_rate': 5,               # Coding rate (4/5)
    'preamble_length': 8,           # Preamble length (8)
    'implicit_header': False,       # Explicit header mode
    'sync_word': 0x12,              # LoRa sync word
    'enable_crc': True              # Enable CRC for error detection
}

# --- SX1276 LoRa Driver Initialization ---
def lora_init():
    # Reset the SX1276
    reset_pin = Pin(lora_pins['reset'], Pin.OUT)
    reset_pin.value(0)
    time.sleep(0.01)  # Short delay
    reset_pin.value(1)
    # Initialize the SX1276 LoRa driver with default parameters
    lora = sx127x.SX127x(spi=lora_spi, pins=lora_pins, parameters=lora_default)
    # Confirm initialization
    print("LoRa modem initialized with default parameters.")
    return lora

