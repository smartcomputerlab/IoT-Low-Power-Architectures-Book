def calculate_lora_data_rate(sf, bw, cr):
    """
    Calculate the LoRa user data rate.
    :param sf: Spreading Factor (integer, typically 7 to 12)
    :param bw: Bandwidth in Hz (e.g., 125000 for 125 kHz)
    :param cr: Coding Rate as a fraction (e.g., 4/5 is 0.8)
    :return: Data rate in bits per second (bps)
    """
    # Data rate formula
    data_rate = (sf * bw) / (2 ** sf) * cr
    return data_rate

if __name__ == "__main__":
    # Prompt user for inputs
    try:
        sf = int(input("Enter Spreading Factor (7-12): "))
        bw = int(input("Enter Bandwidth in Hz (e.g., 125000 for 125 kHz): "))
        cr = float(input("Enter Coding Rate as a fraction (e.g., 0.8 for 4/5): "))
        # Validate inputs
        if sf < 7 or sf > 12:
            raise ValueError("Spreading Factor must be between 7 and 12.")
        if bw <= 0:
            raise ValueError("Bandwidth must be a positive integer.")
        if not (0 < cr <= 1):
            raise ValueError("Coding Rate must be a fraction between 0 and 1.")
        # Calculate data rate
        data_rate = calculate_lora_data_rate(sf, bw, cr)
        # Display the result
        print(f"LoRa Data Rate: {data_rate:.2f} bps")
    except ValueError as e:
        print(f"Input error: {e}")
        
        