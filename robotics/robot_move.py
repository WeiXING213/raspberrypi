import RPi.GPIO as gpio
import time
import sys
import readchar

pwm2 = 0
pwm2_value = 50
def init_servo():
   global pwm2
   global pwm2_value

   gpio.setmode(gpio.BOARD)
   gpio.setup(12, gpio.OUT)
   pwm2 = gpio.PWM(12, pwm2_value)
   pwm2.start(5)

def init():
    gpio.setmode(gpio.BOARD)
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
    #time.sleep(1)
    duty = float(angle)/(180/(12.5-2.5)) + 2.5
    print ("angle = %s, duty cycle = %s"%(angle, duty))
    """ pwm.ChangeDutyCycle(duty) """
    pwm.ChangeDutyCycle(duty)

def key_input(key_press):
    init()
    sleep_time = 0.2
    global pwm2
    global pwm2_value

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
        pwm2_value -= 5
        change_duty(pwm2, pwm2_value)
    elif key_press.lower() == 'k':
        pwm2_value += 5
        change_duty(pwm2, pwm2_value)
    elif key_press.lower() == 'p':
        gpio.cleanup()
        pwm2.stop()
        sys.exit(0);
print "-------------------------------------------------------------------------------------------------------------------"
print "car : z - forward | s - reverse | q - turn left | d - turn right | a - turn left | e - pivot right | i - pivot left"
print "camera : i - look up | k - look down | o - look left | m - look right"
print "\np - exit"
print "-------------------------------------------------------------------------------------------------------------------"


init_servo()
while True:
    init()
    key_input(readchar.readkey())
