# Sixfab - Reading GPS data with Python
# 2020


from time import sleep
import serial

def setup():
    port = "/dev/ttyUSB2"
    ser = serial.Serial(port, 115200, timeout=5)

def getRSSI(ser):
    #port = "/dev/ttyUSB2"
    #ser = serial.Serial(port, 115200, timeout=5)
    ser.write("AT+CSQ\r".encode())
    response = ser.read(64)
    number1 = response[8: 10]
    split1 = str(number1).split("'")
    print("RSSI 1= ", split1[1])
    #ser.close()
    return split1[1]


def getRSRP(ser):
    #port = "/dev/ttyUSB2"
    #ser = serial.Serial(port, 115200, timeout=5)
    ser.write("AT+CESQ\r".encode())
    response = ser.read(64)
    split = str(response).split(",")
    split2 = str(split[5][0: 3]).split("\\")
    print("RSRP = ", split2[0])
    #ser.close()
    return split2[0]

def getMONI(ser):
    ser.write("AT#MONI=7\r".encode())
    response = ser.read(64)
    ser.write("AT#MONI\r".encode())
    response = ser.read(5000)
    response = str(response).split(' ')
    return response

def getMONIQ(ser):
    ser.write("AT#MONI=?\r".encode())
    response = ser.read(64)
    return response

def close():
    ser.close()
#getRSSI()
#getRSRP()
                                           