from adafruit_motorkit import MotorKit
kit = MotorKit()
from time import sleep
from approxeng.input.selectbinder import ControllerResource


print("████████╗██████╗  █████╗  ██████╗██╗  ██╗     ██████╗  ██████╗ ████████╗")
print("╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝     ██╔══██╗██╔═══██╗╚══██╔══╝")
print("   ██║   ██████╔╝███████║██║     █████╔╝█████╗██████╔╝██║   ██║   ██║   ")
print("   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗╚════╝██╔══██╗██║   ██║   ██║   ")
print("   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗     ██████╔╝╚██████╔╝   ██║   ")
print("   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═════╝  ╚═════╝    ╚═╝   ")

def set_speeds(power_left, power_right):
    kit.motor1.throttle = -power_left
    kit.motor2.throttle = power_left
    kit.motor3.throttle = -power_right
    kit.motor4.throttle = -power_right

def stop_motors():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0
    print('Motors stopping')

class RobotStopException(Exception):
    """
    The simplest possible subclass of Exception, we'll raise this if we want to stop the robot
    for any reason. Creating a custom exception like this makes the code more readable later.
    """
    pass

max_power=100

def mixer(yaw, throttle):
    """
    Mix a pair of joystick axes, returning a pair of wheel speeds. This is where the mapping from
    joystick positions to wheel powers is defined, so any changes to how the robot drives should
    be made here, everything else is really just plumbing.
    
    :param yaw: 
        Yaw axis value, ranges from -1.0 to 1.0
    :param throttle: 
        Throttle axis value, ranges from -1.0 to 1.0
    :param max_power: 
        Maximum speed that should be returned from the mixer, defaults to 100
    :return: 
        A pair of power_left, power_right integer values to send to the motor driver
    """
    left = throttle + yaw
    right = throttle - yaw
    scale = float(max_power) / max(1, abs(left), abs(right))
    return int(left * scale), int(right * scale)

gripper_value = 450

try:
    while True:
        # Inner try / except is used to wait for a controller to become available, at which point we
        # bind to it and enter a loop where we read axis values and send commands to the motors.
        try:
            # Bind to any available joystick, this will use whatever's connected as long as the library
            # supports it.
            with ControllerResource(dead_zone=0.1, hot_zone=0.2) as joystick:
                print('Controller found, press HOME button to exit, use left stick to drive.')
                print(joystick.controls)
                # Loop until the joystick disconnects, or we deliberately stop by raising a
                # RobotStopException
                while joystick.connected:
                    # Get joystick values from the left analogue stick
                    x_axis, y_axis = joystick['rx', 'ly']
                    # Get power from mixer function
                    power_left, power_right = mixer(yaw=x_axis, throttle=y_axis)
                    # Set motor speeds
                    set_speeds(-power_left/100, power_right/100)
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
