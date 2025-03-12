import machine
import time

# Get the RTC object
rtc = machine.RTC()

# Read the current memory contents
rtc_mem = rtc.memory()

if len(rtc_mem) == 0:
    # If empty, this is the first cycle
    cycle = 0
else:
    # Convert stored bytes to integer
    cycle = int(rtc_mem.decode())
# Print the current cycle count
print("Current cycle count:", cycle)
# Increment the cycle counter
cycle += 1

# Save the new cycle count to RTC memory
rtc.memory(str(cycle).encode())

# Sleep for 6 seconds
print("Going to deep sleep for 6 seconds...")
time.sleep_ms(1000)  # small delay before entering sleep
machine.deepsleep(6*1000)
