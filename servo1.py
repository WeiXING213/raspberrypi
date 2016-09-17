import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
pwm = GPIO.PWM(7,50)
pwm.start(2.5)
time.sleep(5)

def update(angle):
    """angle value from 10 to 180 """
    time.sleep(1)
    duty = float(angle)/(180/(12.5-2.5)) + 2.5
    print ("angle = %s, duty cycle = %s"%(angle, duty))
    pwm.ChangeDutyCycle(duty)

if __name__ == '__main__':
    try:
        for x in range(180):
            update(x)
        pwm.stop()
     
    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()
