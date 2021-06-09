'''
captureCommands.py
John Keller, Brian Arnold, Yujen Chen
EE 497/498 T-Mobile Drone Detection Capstone Project
6/9/2021

This script is designed to run on a Raspberry Pi 4 Computer with an Sixfab
"IoT Base Hat" attachment, equipped with a Telit LE910C1 Mini PCIe LTE CAT1 Module.

This script supports csvOutput.py to collect connection data from the cellular modem.
Please put this script in the same directory as csvOuput.py (or include path to this
file).

This script will output a CSV file when it is finished containing the captured data in
the same folder containing csvOutput.py.

'''
# Sixfab - Reading GPS data with Python
# 2020


from time import sleep
import serial

def getRSSI(ser):

    ser.write("AT+CSQ\r".encode())
    response = ser.read(64)
    number1 = response[8: 10]
    split1 = str(number1).split("'")
    print("RSSI 1= ", split1[1])
    return split1[1]


def getRSRP(ser):

    ser.write("AT+CESQ\r".encode())
    response = ser.read(64)
    split = str(response).split(",")
    split2 = str(split[5][0: 3]).split("\\")
    print("RSRP = ", split2[0])
    return split2[0]

def getMONI(ser):

    ser.write("AT#MONI\r".encode())
    response = ser.read(5000)
    response = str(response).split(' ')
    print(response)
    return response

    #returns pos N/S pos, E/W pos, altitude, speed (km/hr)
def getGPSACP(ser):

    ser.write("AT$GPSACP\r".encode())
    response = ser.read(5000)
    response = str(response).split(",")
    print(response)
    return response[1], response[2], response[4], response[7]

def getMONIQ(ser):
    ser.write("AT#MONI=?\r".encode())
    response = ser.read(64)
    return response                                    