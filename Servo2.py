from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
from time import sleep
kit = PWM(0x60)
kit.servo[15].angle = 90