'''
csvOutput.py
John Keller, Brian Arnold, Yujen Chen
EE 497/498 T-Mobile Capstone Project
4/20/2021
'''

#imports
from datetime import datetime
import csv
import time
from captureCommands import *
import serial
import statistics
print("Program Starting")

#User set parameters
captureMinutes = 7 # how long to capture data for
actualRate = 0 # added capture delay (in seconds)
isThisADrone = 1 #1 for drone, 0 for non-drone
startDelay = 5 #delay in minutes from program start to data capture

time_data = [] #Time elasped
rssi_data = [] #RSSI measurements (signal strength)
num_cell_towers_data = [] #number of connect cell phone towers
drone_det_data = [] #0/1 (not drone, drone)
moni_data = [] #RSRP data (from serving and non serving cells
speed_data = [] #km/hr
altitude_data = [] #meters
longitude_data = [] #format = dddmmm.mmmm E/W (d = degrees, m = minutes)
latitude_data = [] #format = ddmm.mmmm N/S (d = degrees, m = minutes)
std_dev_rsrp = [] #std dev of all rsrp from neighbooring and serving cells

port = "/dev/ttyUSB2"

#Initializing serial port/AT commands
ser = serial.Serial(port, 115200, timeout=5)
ser.write("AT$GPSRST\r".encode())
response = ser.read(64)
ser.write("AT$GPSP=1\r".encode())
response = ser.read(64)
ser.write("AT#MONI=7\r".encode())
response = ser.read(64)
print("Wait for GPS to connect")
time.sleep(60 * startDelay) #For GPS
print("GPS wait over")

#parameter convserion
duration = 60 * captureMinutes
RSSI_offset = -113

#start timer
startTime = time.perf_counter()

while duration > (time.perf_counter() - startTime):
    #Performs calculation to get RSSI in db from code
    rssi_data.append(int(getRSSI(ser)) * 2 + RSSI_offset)
                                       
    #Raw (unformatted/calculated) RSRP data
    moni_data.append(getMONI(ser))
    
    #lat, long, altitude, speed
    single_GPS_data = getGPSACP(ser)
    latitude_data.append(single_GPS_data[0])
    longitude_data.append(single_GPS_data[1])
    altitude_data.append(single_GPS_data[2])
    speed_data.append(single_GPS_data[3])
    
    #time elasped
    time_data.append(time.perf_counter() - startTime)
    
    #optional added delay
    print("Time Left = ", duration - (time.perf_counter() - startTime))
    time.sleep(actualRate)


#calculates difference in RSRP between serving and most powerful
#non-serving cell
arrayRSRP = []
flag2RSRP = 0

for measurement in moni_data:
    servingRSRP, neighborRSRP = float("-inf"), float("-inf")
    flagRSRP = 0
    flag2RSRP = 0
    all_rsrp = []
    #print("Set = ", measurement)
    for text in measurement: 
        split = text.split(":")
        #print("To split = ", split)
        if (split[0] == "RSRP" and (int(split[1]) != 0)):
            if (flagRSRP == 0):
                servingRSRP = int(split[1])
                flagRSRP = 1
                all_rsrp.append(servingRSRP)
            elif (flag2RSRP == 0):
                flag2RSRP = 1
            else:
                neighborRSRP = max(neighborRSRP, int(split[1]))
                all_rsrp.append(int(split[1]))
    #print("Neighbor = ", neighborRSRP)
    #print("Serving = ", servingRSRP)
    arrayRSRP.append(servingRSRP - neighborRSRP)
    if (len(all_rsrp) == 0):
        std_dev_rsrp.append(0)
    elif (len(all_rsrp) == 1):
        std_dev_rsrp.append(0)
    else:   
        std_dev_rsrp.append(statistics.stdev(all_rsrp))
#print("Diff in RSRP = ", arrayRSRP)

#adds drone/non-drone classification to array with same length as other measurements
captures = len(rssi_data)
for i in range(0, captures):
    drone_det_data.append(isThisADrone)
    
#closes serial port
ser.close()

#creates custom file name for output CSV data file
dateString = datetime.now()
filename = "dataCapture " + str(dateString)[:13] + ";" + str(dateString)[14:16] + ";" + str(dateString)[17:19] + ".csv"

#writes data to output CSV File
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["RSSI, Delt RSRP, Std Dev RSRP, Lat, Long, Altitude, Speed, Classification, Time Elasped, Moni Data"])
    for i in range(0, len(rssi_data)):
        row = []
        row.append(rssi_data[i])
        row.append(arrayRSRP[i])
        row.append(std_dev_rsrp[i])
        row.append(latitude_data[i])
        row.append(longitude_data[i])
        row.append(altitude_data[i])
        row.append(speed_data[i])
        row.append(drone_det_data[i])
        row.append(time_data[i])
        row.append(moni_data[i])
        writer.writerow(row)
    #writer.writerow(rssi_data)  #writes RSSI data
    #writer.writerow(arrayRSRP)  #writes RSRP data
    #writer.writerow(std_dev_rsrp) #standard deviation of rsrp values


    #writer.writerow(latitude_data)  #writes latitude data
    #writer.writerow(longitude_data)  #writes longitude data
    #writer.writerow(altitude_data)  #writes altitude data
    #writer.writerow(speed_data)  #writes speed data
    
    #writer.writerow(drone_det_data) #writes drone classification (0/1)
    #writer.writerow(time_data)     #writes time

print("Capture done, CSV file created with name ", str(filename))