from __future__ import division
import time

import Adafruit_PCA9685

pwm0 = Adafruit_PCA9685.PCA9685(address=0x60)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 450  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(pwmno,channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    if pwmno == 0:
        pwm0.set_pwm(channel, 0, pulse)
    elif pwmno == 1:
        pwm1.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm0.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    # Move servo on board 0 channel O between extremes.
    pwm0.set_pwm(15, 0, servo_min)
    time.sleep(5)
    pwm0.set_pwm(15, 0, servo_max)
    time.sleep(5)
