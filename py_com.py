#!/usr/bin/python3
import rospy
from std_msgs.msg import Float32
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
        time.sleep(0.5)
        while ser.inWaiting()>0 and len(res)<=2:
            res += (ser.read(1)).decode()
            print(res)
        if res=="03":
            print("Device with id=03 found!")
            break
        else:
            ser.close()
            print("connection to "+port+" closed")
    except srl.serialutil.SerialException:
        print("connection to "+port+" failed")
        if i!=last_number_of_port_name:
            pass
        else:
            print("Cant find id=03 device")
            print("Exit: 1")
            exit(1)

pub = rospy.Publisher('/wheel_module', Float32, queue_size=10)
rospy.init_node('wheel_module')

res = ""
cm_teak = "/teak;".encode()
time_start = time.time()
print("Well done!")
while True:
    ser.write(cm_teak)
    time.sleep(0.025)
    while ser.inWaiting() > 0:
        res += (ser.read(1)).decode()
    less, numb = res.split(" ")
    if not rospy.is_shutdown():
        rospy.loginfo(float(numb))
        pub.publish(float(numb))
        #rate.sleep()
    print("{"+res+" "+str(time.time()-time_start)+" seconds }")
    res = ""
