from adafruit_motorkit import MotorKit
kit = MotorKit()
import time.sleep

kit.motor1.throttle = 1.0
sleep(1)
kit.motor1.throttle = 0