import machine

def get_chip_id():
    """Retrieve the unique chip ID from the ESP32."""
    chip_id = machine.unique_id()  # Returns a bytes object
    return chip_id

def chip_id_to_ascii(chip_id):
    """
    Convert chip ID (bytes) to a human-readable ASCII-based name.
    It maps byte values to printable characters.
    """
    name = ''.join(chr((b % 26) + 65) for b in chip_id)  # Maps to A-Z
    return name

# Get chip ID
chip_id = get_chip_id()
# Convert to ASCII-based name
chip_name = chip_id_to_ascii(chip_id)
# Display results
print(f"Chip ID (Raw): {chip_id.hex()}")
print(f"Generated Name: {chip_name}")
