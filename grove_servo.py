import RPi.GPIO as IO
import sys
import time
from numpy import interp

IO.setwarnings(False)
IO.setmode(IO.BCM)

class GroveServo:
    MIN_DEGREE = 0
    MAX_DEGREE = 180
    INIT_DUTY = 2.5

    def __init__(self, channel):
        IO.setup(channel,IO.OUT)
        self.pwm = IO.PWM(channel,50)
        self.pwm.start(GroveServo.INIT_DUTY)

    def __del__(self):
        self.pwm.stop()

    def setAngle(self, angle):
        # Map angle from range 0 ~ 180 to range 25 ~ 125
        angle = max(min(angle, GroveServo.MAX_DEGREE), GroveServo.MIN_DEGREE)
        self.pwm.ChangeDutyCycle(angle)

Grove = GroveServo

def main():
    #for x in range(0, 45):
    #    servo.setAngle(2.5)
    #    time.sleep(0.01)
        
    #time.sleep(0.25)

    #for x in range(0, 45):
    #    servo.setAngle(12.5)
    #    time.sleep(0.01)

    # HARDCODED PIN ON GROVE HAT
    pin = 12
    servo = GroveServo(pin)
    
    for x in range(0, 45):
        servo.setAngle(0)
        time.sleep(0.01)

    time.sleep(0.25)

    for x in range(0, 45):
        servo.setAngle(75)
        time.sleep(0.01)

if __name__ == '__main__':
    main()
