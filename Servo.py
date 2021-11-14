from __future__ import division
import time

from approxeng.input.selectbinder import ControllerResource

import Adafruit_PCA9685

pwm0 = Adafruit_PCA9685.PCA9685(address=0x60)

# Configure min and max servo pulse lengths
servo_min = 130  # Min pulse length out of 4096
servo_max = 280  # Max pulse length out of 4096
servo_start = 200

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

#print('Moving servo on channel 0, press Ctrl-C to quit...')
#while True:
#    # Move servo on board 0 channel O between extremes.
#    pwm0.set_pwm(15, 0, servo_min)
#    time.sleep(5)
#    pwm0.set_pwm(15, 0, servo_max)
#    time.sleep(5)

pwm0.set_pwm(15, 0, servo_start)

try:
    while True:
        try:
            with ControllerResource(dead_zone=0.1, hot_zone=0.2) as joystick:
                print('Controller found, press HOME button to exit, use left stick to drive.')
                print(joystick.controls)
                while joystick.connected:
                    x_axis, y_axis, servo_axis = joystick['rx', 'ry', 'lx']
                    servo_start = servo_start + round(servo_axis)
                    pwm0.set_pwm(15, 0, servo_start)
                    #power_left, power_right = mixer(yaw=x_axis, throttle=y_axis)
                    #set_speeds(-power_left/100, power_right/100)
                    # Get a ButtonPresses object containing everything that was pressed since the last
                    # time around this loop.
                    joystick.check_presses()
                    # Print out any buttons that were pressed, if we had any
                    if joystick.has_presses:
                    # If home was pressed, raise a RobotStopException to bail out of the loop
                    # Home is generally the PS button for playstation controllers, XBox for XBox etc
                        if 'home' in joystick.presses:
                            raise RobotStopException()
                        if 'ddown' in joystick.presses:
                            if max_power > 50:
                                max_power = max_power - 10
                                print("Set to", max_power, "% speed")
                            else:
                                print("Already minimum speed")
                        if 'dup' in joystick.presses:
                            if max_power < 100:
                                max_power = max_power + 10
                                print("Set to", max_power, "% speed")
                            else:
                                print("Already maximum speed")
        except IOError:
            # We get an IOError when using the ControllerResource if we don't have a controller yet,
            # so in this case we just wait a second and try again after printing a message.
            print('No controller found yet')
            sleep(1)
except RobotStopException:
    # This exception will be raised when the home button is pressed, at which point we should
    # stop the motors.
    stop_motors()
