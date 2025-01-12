#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
ihpmil1=float(input("Input average current value for high power stage in mA (case1): "))
ihpmil2=float(input("Input average current value for high power stage in mA (case2): "))
thp1=float(input("Input time of high power stage in sec (case1): "))
thp2=float(input("Input time of high power stage in sec (case2): "))
ilp1=float(input("Input average current value for low power stage in µA (case1): "))
ihpmic1 = ihpmil1*1000.0  # current high power in µA
ihpmic2 = ihpmil2*1000.0  # current high power in µA
avi1 = np.arange(ilp1+1.0,1500.0, 10.0)  # average current in µA
avi2 = np.arange(ilp1+1.0,1500.0, 10.0)  # average current in µA
tlp1=thp1*(ihpmic1-avi1)/(avi1-ilp1)
tlp2=thp2*(ihpmic2-avi2)/(avi2-ilp1)
#create data
x1 = [1,10,100,1000,10000,100000]
y1 = [100,100,100,100,100,100]
x2 = [1,10,100,1000,10000,100000]
y2 = [1000,1000,1000,1000,1000,1000]
fig, ax = plt.subplots()
plt.yscale("log")
ax.grid()
ax.set(ylabel='time in seconds', xlabel='average current in µA',title='low_power time')
ax.plot(avi1, tlp1, label="LoRa long")
ax.plot(avi2, tlp2, label="LoRa short")
ax.plot(y1,x1,label="VLP")
ax.plot(y2,x2,label="LP")
plt.legend()
fname=str(input("Give the name of the graph file: "))
fig.savefig(fname)
plt.show()
