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
z_plus.direction = digitalio.Direction.INPUT
z_minus.direction = digitalio.Direction.INPUT

z_motor = pwmio.PWMOut(board.A2, duty_cycle_cycle=2 ** 15, frequency=50)

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
