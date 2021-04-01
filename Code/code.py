import board
import digitalio
import analogio
import time
import pwmio
from adafruit_motor import servo
from adafruit_motor import stepper

DELAY = 0.01
STEPS = 200

# Setup Joystick pins
x_plus = digitalio.DigitalInOut(board.GP0)
x_minus = digitalio.DigitalInOut(board.GP1)
y_plus = digitalio.DigitalInOut(board.GP2)
y_minus = digitalio.DigitalInOut(board.GP3)

# Setup Joystick pins as input
x_plus.direction = digitalio.Direction.INPUT
x_minus.direction = digitalio.Direction.INPUT
y_plus.direction = digitalio.Direction.INPUT
y_minus.direction = digitalio.Direction.INPUT

# Setup z movement pins
z_up = digitalio.DigitalInOut(board.GP4)
z_down = digitalio.DigitalInOut(board.GP5)

# Setup z movement pins as input
z_up.direction = digitalio.Direction.INPUT
z_down.direction = digitalio.Direction.INPUT

# Setup stepper pwm pin
pwm = pwmio.PWMOut(board.GP14, duty_cycle_cycle=2 ** 15, frequency=50)

# Setup z motor
my_servo = servo.Servo(pwm)

# Setup x motor pins
x_coils = (
    digitalio.DigitalInOut(board.GP6),  # A1
    digitalio.DigitalInOut(board.GP7),  # A2
    digitalio.DigitalInOut(board.GP8),  # B1
    digitalio.DigitalInOut(board.GP9),  # B2
)
# Setup y motor pins
y_coils = (
    digitalio.DigitalInOut(board.GP10),  # A1
    digitalio.DigitalInOut(board.GP11),  # A2
    digitalio.DigitalInOut(board.GP12),  # B1
    digitalio.DigitalInOut(board.GP13),  # B2
)


# Setup x and y motor pin direction
for coil in x_coils:
    coil.direction = digitalio.Direction.OUTPUT
for coil in y_coils:
    coil.direction = digitalio.Direction.OUTPUT

# Setup x motor
x_motor = stepper.StepperMotor(
    x_coils[0], x_coils[1], x_coils[2], x_coils[3], microsteps=None
)
x_motor.release()

# Setup y motor
y_motor = stepper.StepperMotor(
    y_coils[0], y_coils[1], y_coils[2], y_coils[3], microsteps=None
)
y_motor.release()

# Setup movement variables
angle = 0
my_servo.angle = 0
time.sleep(1)


while True:
    if x_plus.value:
        x_motor.onestep(direction=stepper.FORWARD)
    elif x_minus:
        x_motor.onestep(direction=stepper.BACKWARD)

    if y_plus.value:
        y_motor.onestep(direction=stepper.FORWARD)
    elif y_minus.value:
        y_motor.onestep(direction=stepper.BACKWARD)

    if z_up.value:
        if angle + 5 < 180:
            angle += 5
            my_servo.angle = angle
    elif z_down.value:
        if angle - 5 > 0:
            angle -= 5
            my_servo.angle = angle
    time.sleep(0.01)