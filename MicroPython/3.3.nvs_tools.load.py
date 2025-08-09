# nvs_tools.load.py
from nvs_tools  import *

nvs_key="param"
ts_param=ustruct.pack("i16s",1538804,"YOX31M0EDKO0JATK")
pow_param=ustruct.pack("2i4f",1,64,0.01,0.2,26.5,15.5)

write_nvs_ts(nvs_key,ts_param)
write_nvs_power(nvs_key,pow_param)

