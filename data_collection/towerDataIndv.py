'''
towerDataIndv.py
John Keller, Brian Arnold, Yujen Chen
EE 497/498 T-Mobile Drone Detection Capstone Project
6/9/2021

This script takes raw moni data from a CSV output file created and formats it
to be viewed by connected towers and their RSRP value over time. This can be useful
for looking at connection power of specific cell phone towers over time.

This script can also seperate RSRQ by tower if minor modifications are made.

Please be sure to look at line 40 and make sure the index matches the row of the MONI measurment
in the input CSV file.

This script will output a CSV file when it is finished containing the captured data in
the same folder containing csvOutput.py. Please put input CSV file in the same folder as
towerDataIndv.py.

This script will output the new CSV file in the same directory it is located. 

'''

import csv

moni_data = []

ids = {}
name = 'dataCapture 2021-05-02 13;41;02.-8StoryOutsideCaptureRoofSouth' #Name of input file
file = name + '.csv'

#open file, get raw moni data
with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            moni_data.append(row[9]) #change this value to the row that MONI measurement occupies in input CSV file

#Gets ids of all towers seen by SIM
for measurement in moni_data:
    array = measurement.split(",")
    cellId = ""
    earfcn = ""
    startFlag = False
    for value in array:
        split = value.split(":")
        if (len(split) > 1):
            measType = split[0][2:]
            measVal = split[1][:len(split[1]) - 1]
            if (measType == "PhysCellId"):
                cellId = str(measVal)
            elif (measType == "EARFCN"):
                earfcn = measVal
                if (startFlag == False):
                    earfcn = ""
                    cellId = ""
                    startFlag = True
                elif (cellId != "0000000"):
                    id = cellId + "-" + earfcn
                    if (id not in ids):
                        ids[id] = []
ids["Serving Cell"] = []

#Seperate signal strgenth data by tower per cycle of detections
#Add in "0" if measurement from particular id is not seen in a cycle
for measurement in moni_data:
    array = measurement.split(",")
    lastRSRP = ""
    cellId = ""
    earfcn = ""
    startFlag = False
    firstValue = True
    count = 0
    for value in array:
        split = value.split(":")
        if (len(split) > 1):
            measType = split[0][2:]
            measVal = split[1][:len(split[1]) - 1]

            if (measType == "PhysCellId"):
                cellId = str(measVal)

            elif (measType == "EARFCN"):
                earfcn = measVal
                if (startFlag == False):
                    earfcn = ""
                    cellId = ""
                    startFlag = True

                elif (cellId != "0000000"):
                    id = cellId + "-" + earfcn
                    ids[id].append(lastRSRP)

                if (count == 1):
                    ids["Serving Cell"].append(cellId + "-" + earfcn)
                count += 1

            elif (measType == "RSRP"):
                lastRSRP = measVal
    maxLen = 0
    firstValue = True
    for key, value in ids.items():
        maxLen = max(maxLen, len(value))

    for key, value in ids.items():
        if (len(value) != maxLen):
            value.append("0")
    count = 0

print(ids)

# writes data to output CSV File. Output will be the same name with "Towers" appended to the end
keys = list(ids.keys())
length = len(ids[keys[0]])
with open(name + 'Towers' + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(keys)
    for i in range(length):
        row = []
        for key in keys:
            row.append(ids[key][i])
        writer.writerow(row)