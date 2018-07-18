#!/usr/bin/python3

import serial as srl
import time

last_number_of_port_name = 11
port = ""
cm_id = "/id;".encode()
for i in range(0,last_number_of_port_name+1):
    try:
        res = ""
        port = "/dev/ttyACM"+str(i)
        print("try connect to "+port)
        ser = srl.Serial(port)
        ser.baudrate = 115200
        print("Well done!")
        ser.write(cm_id)
        time.sleep(0.1)
        while ser.inWaiting()>0 and len(res)<=2:
            res += ser.read(1)
        if res=="03":
            print("Device with id=03 found!")
            break
        else:
            ser.close()
            print("idc what is it"+res)
    except srl.serialutil.SerialException:
        print("connection to"+port+" failed")
        if last_number_of_port_name!=11:
            pass
        else:
            print("Cant find id=03 device")
            print("Exit: 1")
            exit(1)

if ser.isopen():
    res = ""
    cm_teak = "/teak;".encode()
    time_start = time.time()
    print("Well done!")
    while True:
        ser.write(cm_teak)
        time.sleep(1)
        while ser.inWaiting() > 0:
            res += ser.read(1)
        print("{"+res+" "+str(time.time()-time_start)+" seconds }")
        res = ""
else:
    print("idc, but serial is not open")
