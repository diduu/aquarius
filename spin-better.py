from time import sleep
import pigpio
import signal
import sys

DIR = 20  # Direction GPIO Pin
STEP = 21  # Step GPIO Pin

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

# Set Microstepping mode
MODE = (14, 15, 18)  # Microstep Resolution GPIO Pins
RESOLUTION = {
    "Full": (0, 0, 0),
    "Half": (1, 0, 0),
    "1/4": (0, 1, 0),
    "1/8": (1, 1, 0),
    "1/16": (0, 0, 1),
    "1/32": (1, 0, 1),
}

for i, pin in enumerate(MODE):
    pi.write(pin, RESOLUTION["Full"][i])

# Set direction (1 for clockwise, 0 for anti-clockwise)
pi.write(DIR, 1)

# Set duty cycle and frequency
pi.set_PWM_dutycycle(STEP, 255 // 2)  # On-off half of the time
pi.set_PWM_frequency(STEP, 500)  # 500 pulses per second


def exit_function(sig, frame):
    print("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
    pi.set_PWM_dutycycle(STEP, 0)  # PWM off
    pi.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, exit_function)
signal.pause()
