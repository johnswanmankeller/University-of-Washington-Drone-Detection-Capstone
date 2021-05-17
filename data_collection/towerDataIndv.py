'''
Name: John Keller
Purpose: Takes raw moni data from csv, returns signal
strength measurement from individual tower as well as
serving cell id over time
Date: 5/10/2021
'''
import csv

moni_data = []

ids = {}
name = 'dataCapture 2021-05-02 13;41;02.-8StoryOutsideCaptureRoofSouth'
file = name + '.csv'

#open file, get raw moni data
with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            moni_data.append(row[9])

#get the ids of all towers seen by SIM
for measurement in moni_data:
    array = measurement.split(",")
    cellId = ""
    earfcn = ""
    startFlag = False
    # ADD CASE FOR NO SERVING CELLS
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

# writes data to output CSV File
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