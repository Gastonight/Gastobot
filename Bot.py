from adafruit_motorkit import MotorKit
kit = MotorKit()
import time

kit.motor1.throttle = 0.5
kit.motor4.throttle = 0.5
time.sleep(1)
kit.motor1.throttle = 0
kit.motor4.throttle = 0.5