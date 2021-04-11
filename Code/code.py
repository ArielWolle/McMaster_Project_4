import board
import digitalio
import analogio
import time
import pwmio
from adafruit_motor import servo
from adafruit_motor import stepper

# Author: Ariel Wolle

# Description:
# This code is to be run on a Raspberry Pi Pico using the wiring diagram included in the wiring folder
# The main function of this code is to control a 3 axis CNC painting machine for my ENG1P13 University Course

# Input provided to the user:
# 8-axis Joystick that uses 4 microswitches as an input (GPIO2-5)
# 2 Arcade style buttons that use 2 microswitches as an input (GPOI19-20)

# Input used by the machine:
# 4 limit switches that act as endstops for the CNC machine (GPIO14-17)

# Outputs:
# 2x4 PWM GPIO for each stepper motors (GPIO6-13)
# 1 PWM GPIO for the Rotational axis servo (GPOI18)

# Setup Joystick pins
x_plus = digitalio.DigitalInOut(board.GP2)
x_minus = digitalio.DigitalInOut(board.GP4)
y_plus = digitalio.DigitalInOut(board.GP3)
y_minus = digitalio.DigitalInOut(board.GP5)

# Setup Joystick pins as input
x_plus.direction = digitalio.Direction.INPUT
x_minus.direction = digitalio.Direction.INPUT
y_plus.direction = digitalio.Direction.INPUT
y_minus.direction = digitalio.Direction.INPUT

x_plus.pull = digitalio.Pull.DOWN
x_minus.pull = digitalio.Pull.DOWN
y_plus.pull = digitalio.Pull.DOWN
y_minus.pull = digitalio.Pull.DOWN

# Setup z movement pins
z_up = digitalio.DigitalInOut(board.GP19)
z_down = digitalio.DigitalInOut(board.GP20)

# Setup z movement pins as input
z_up.direction = digitalio.Direction.INPUT
z_down.direction = digitalio.Direction.INPUT

z_up.pull = digitalio.Pull.DOWN
z_down.pull = digitalio.Pull.DOWN

# Setup stepper pwm pin
pwm_servo = pwmio.PWMOut(board.GP18, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(
    pwm_servo, min_pulse=500, max_pulse=2250
)  # tune pulse for specific servo


# Setup x motor pins
x_coils = (
    pwmio.PWMOut(board.GP6, duty_cycle=2 ** 15, frequency=2000),  # A1
    pwmio.PWMOut(board.GP7, duty_cycle=2 ** 15, frequency=2000),  # A2
    pwmio.PWMOut(board.GP8, duty_cycle=2 ** 15, frequency=2000),  # B1
    pwmio.PWMOut(board.GP9, duty_cycle=2 ** 15, frequency=2000),  # B2
)
# Setup y motor pins
y_coils = (
    pwmio.PWMOut(board.GP10, duty_cycle=2 ** 15, frequency=2000),  # A1
    pwmio.PWMOut(board.GP11, duty_cycle=2 ** 15, frequency=2000),  # A2
    pwmio.PWMOut(board.GP12, duty_cycle=2 ** 15, frequency=2000),  # B1
    pwmio.PWMOut(board.GP13, duty_cycle=2 ** 15, frequency=2000),  # B2
)


# Setup x motor
x_motor = stepper.StepperMotor(
    x_coils[0], x_coils[1], x_coils[2], x_coils[3], microsteps=4
)


# Setup y motor
y_motor = stepper.StepperMotor(
    y_coils[0], y_coils[1], y_coils[2], y_coils[3], microsteps=4
)


# Setup endstop pins
x_plus_endstop = digitalio.DigitalInOut(board.GP14)
x_minus_endstop = digitalio.DigitalInOut(board.GP15)
y_plus_endstop = digitalio.DigitalInOut(board.GP16)
y_minus_endstop = digitalio.DigitalInOut(board.GP17)

# Setup endstop pins as input
x_plus_endstop.direction = digitalio.Direction.INPUT
x_minus_endstop.direction = digitalio.Direction.INPUT
y_plus_endstop.direction = digitalio.Direction.INPUT
y_minus_endstop.direction = digitalio.Direction.INPUT

x_plus_endstop.pull = digitalio.Pull.UP
x_minus_endstop.pull = digitalio.Pull.UP
y_plus_endstop.pull = digitalio.Pull.UP
y_minus_endstop.pull = digitalio.Pull.UP

# Setup movement variables
angle = 100
my_servo.angle = 100
time.sleep(1)

# Main Loops
while True:
    time.sleep(0.001)
    # Check for x movement in joystick and that the pen plotter is not at max/min x
    if x_plus.value and (x_plus_endstop.value):
        x_motor.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
    elif x_minus.value and (x_minus_endstop.value):
        x_motor.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)

    # Check for y movement in joystick and that the pen plotter is not at max/min y
    if y_plus.value and (y_plus_endstop.value):
        y_motor.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
    elif y_minus.value and (y_minus_endstop.value):
        y_motor.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)

    # Checks that only on button is pressed for z movement
    if not (z_up.value and z_down.value):
        # Checks if z value is not at max and up button is pressed
        if z_up.value:
            if angle + 0.2 < 100:
                angle += 0.2
                my_servo.angle = int(angle)
        # Checks if z value is not at min and down button is pressed
        elif z_down.value:
            if angle - 0.2 > 0:
                angle -= 0.2
                my_servo.angle = int(angle)
