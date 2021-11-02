from adafruit_motorkit import MotorKit
kit = MotorKit()
import time

kit.motor1.throttle = 1.0
time.sleep(1)
kit.motor1.throttle = 0