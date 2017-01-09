import RPi.GPIO as gpio
import time
import sys
import readchar
import blescan
import sys
import bluetooth._bluetooth as bluez
from math import *

pwm_value = 90
pwm = 0

pwm_b_value = 90
pwm_b = 0 

def init_servo():
   global pwm_value
   global pwm
   global pwm_b
   global pwm_b_value

   gpio.setmode(gpio.BOARD)
   gpio.setup(12, gpio.OUT)
   pwm = gpio.PWM(12, 50)
   
   gpio.setup(16, gpio.OUT)
   pwm_b = gpio.PWM(16, 50)

   duty = float(pwm_value)/(180/(12.5-2.5)) + 2.5
   pwm.start(duty)
   pwm_b.start(duty)

def active_servo():
    gpio.setmode(gpio.BOARD)
    gpio.setup(12, gpio.OUT)
    gpio.setup(16, gpio.OUT)
    

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)
    
def forward(tf):
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def reverse(tf):
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def turn_left(tf):
    gpio.output(7, True)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def turn_right(tf):
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def pivot_left(tf):
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def pivot_right(tf):
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def change_duty(pwm, angle):
    #time.sleep(1)
    duty = float(angle)/(180/(12.5-2.5)) + 2.5
    print ("angle = %s, duty cycle = %s"%(angle, duty))
    """ pwm.ChangeDutyCycle(duty) """
    pwm.ChangeDutyCycle(duty)

def calculateDistance(rssi):

    txPower = -59

    if (rssi == 0):
        return -1.0

    ratio = rssi * 1.0 / txPower
    if (ratio < 1.0):
        return pow(ratio,10)

    else:
        distance =  (0.89976)*pow(ratio,7.7095) + 0.111;
        return distance;       

def key_input(key_press):
    sleep_time = 0.4
    walking_time = 0.8
    global pwm
    global pwm_value
    global pwm_b
    global pwm_b_value

    if key_press.lower() == 'z':
        init()
        forward(walking_time)
    elif key_press.lower() == 's':
        init()
        reverse(walking_time)
    elif key_press.lower() == 'd':
        init()
        turn_left(sleep_time)
    elif key_press.lower() == 'q':
        init()
        turn_right(sleep_time)
    elif key_press.lower() == 'e':
        init()
        pivot_left(sleep_time)
    elif key_press.lower() == 'a':
        init()
        pivot_right(sleep_time)
    #--servo--
    elif key_press.lower() == 'i':
        active_servo()
        pwm_value -= 5
        change_duty(pwm, pwm_value)
    elif key_press.lower() == 'k':
        pwm_value += 5
        change_duty(pwm,pwm_value)
    elif key_press.lower() == 'j':
        pwm_b_value -= 5
        change_duty(pwm_b, pwm_b_value)
    elif key_press.lower() == 'l':
        pwm_b_value += 5
        change_duty(pwm_b,pwm_b_value)
    #exit
    elif key_press.lower() == 'p':
        gpio.cleanup()
        pwm.stop()
        pwm_b.stop()
        sys.exit(0);
print "-------------------------------------------------------------------------------------------------------------------"
print "car : z - forward | s - reverse | q - turn left | d - turn right | a - turn left | e - pivot right | i - pivot left"
print "camera : i - look up | k - look down | o - look left | m - look right"
print "\np - exit"
print "-------------------------------------------------------------------------------------------------------------------"

init_servo()
#while True:
#    key_input(readchar.readkey())

dev_id = 0
try:
        sock = bluez.hci_open_dev(dev_id)
        print "ble thread started"

except:
        print "error accessing bluetooth device..."
        sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

a = 0
while True:
    returnedList = blescan.parse_events(sock, 10)
    for beacon in returnedList:
        items =  beacon.split(',')

        for i in range(9):
            a =( a + calculateDistance(float(items[5])) )/2
        print a
        if a > 1:
            init()
            forward(0.2)
            print "run forward"
        a = 0
        

"""
video streaming 

recevier : gst-launch-1.0 -v udpsrc port=9000 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! rtph264depay ! video/x-h264,width=640,height=480,framerate=30/1 ! h264parse ! avdec_h264 ! videoconvert ! autovideosink sync=false

sender: pi@raspberrypi:~ $ raspivid -n -w 640 -h 480 -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.0.11 port=9000
"""
