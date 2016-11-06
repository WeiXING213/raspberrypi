import RPi.GPIO as gpio
import time
import sys
import readchar

pwm2 = 0
def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(12, gpio.OUT)
    global pwm2
    pwm2 = gpio.PWM(12, 50)
    pwm2.start(5)
    """
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)
    """
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
    duty = float(angle)/(180/(12.5-2.5)) + 2.5
    print ("angle = %s, duty cycle = %s"%(angle, duty))
    """ pwm.ChangeDutyCycle(duty) """
    pwm.ChangeDutyCycle(duty)

def key_input(key_press):
    init()
    sleep_time = 0.2
    global pwm2
    
    if key_press.lower() == 'z':
        forward(sleep_time)
    elif key_press.lower() == 's':
        reverse(sleep_time)
    elif key_press.lower() == 'q':
        turn_left(sleep_time)
    elif key_press.lower() == 'd':
        turn_right(sleep_time)
    elif key_press.lower() == 'a':
        pivot_left(sleep_time)
    elif key_press.lower() == 'e':
        pivot_right(sleep_time)
   
    elif key_press.lower() == 'i':
        change_duty(pwm2, 30)
        #pwm2.ChangeDutyCycle(7.5)

    elif key_press.lower() == 'k':
        change_duty(pwm2, 100)
        #pwm2.ChangeDutyCycle(5)


    elif key_press.lower() == 'p':
        gpio.cleanup()
        sys.exit(0);

while True:
    init()
    key_input(readchar.readkey())
