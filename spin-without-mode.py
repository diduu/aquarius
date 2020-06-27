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
