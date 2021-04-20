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