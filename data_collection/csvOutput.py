'''
csvOutput.py
John Keller
EE 497/498 T-Mobile Capstone Project
3/11/2021
'''
#from cellulariot import cellulariot
from datetime import datetime
import csv
import time
from GPS import *
import serial

dateString = datetime.now()
print("Program Starting")
#User set parameters
captureMinutes = 1.1 # how long to capture data for
actualRate = 0 # added capture delay (in seconds)
isThisADrone = 0 #1 for drone, 0 for non-drone

x_data = []
y1_data = []
y2_data = []
drone_det_data = []
moni_data = []


port = "/dev/ttyUSB2"
ser = serial.Serial(port, 115200, timeout=5)
ser.write("AT#MONI=7\r".encode())
response = ser.read(64)




#parameter convserion
duration = 60 * captureMinutes

#start timer
startTime = time.perf_counter()
while duration > (time.perf_counter() - startTime):
    y1_data.append(getRSSI(ser))
    #y2_data.append(getRSRP(ser))
    x_data.append(time.perf_counter() - startTime)
    moni_data.append(getMONI(ser))
    print("MONI Info = ",  getMONI(ser))
    print("Number of Cells = ", getMONIQ(ser))
    time.sleep(actualRate)

     
arrayRSRP = []
flag2RSRP = 0
for measurement in moni_data:
    servingRSRP, neighborRSRP = float("-inf"), float("-inf")
    flagRSRP = 0
    flag2RSRP = 0 
    print("Set = ", measurement)
    for text in measurement: 
        split = text.split(":")
        print("To split = ", split) 
        if (split[0] == "RSRP" and (int(split[1]) != 0)):
            if (flagRSRP == 0):
                servingRSRP = int(split[1])
                flagRSRP = 1
            elif (flag2RSRP == 0):
                flag2RSRP = 1
            else:
                neighborRSRP = max(neighborRSRP, int(split[1]))
    print("Neighbor = ", neighborRSRP)
    print("Serving = ", servingRSRP)
    arrayRSRP.append(servingRSRP - neighborRSRP)
print("Diff in RSRP = ", arrayRSRP)


time.sleep(actualRate)
#putting data in correct format
y1_result = []
y2_result = []
print("raw y1_data = ", y1_data)
print("raw y2_data = ", y2_data)

    
captures = len(y1_data)
RSSI_offset = -113
    
for i in range(0, captures):
    y1_result.append(int(y1_data[i]) * 2 + RSSI_offset)   
    #y2_result.append(arrayRSRP[i])
    drone_det_data.append(isThisADrone)
    
print("final y1_data = ", y1_result)
print("final y2_data = ", y2_result)
ser.close()


#
#filename in format "dataCapture 2021-03-11 15;18;29.csv"
# = datetime.now()
filename = "dataCapture " + str(dateString)[:13] + ";" + str(dateString)[14:16] + ";" + str(dateString)[17:19] + ".csv"

with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(y1_result)  #writes RSSI data
    writer.writerow(arrayRSRP)  #writes RSRP data
    writer.writerow(drone_det_data) #
    writer.writerow(x_data)     #writes time

print("Capture done, CSV file created with name ", str(filename))