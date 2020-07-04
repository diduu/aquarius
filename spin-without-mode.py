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


pi.write(DIR, 1) # Set direction (1 for clockwise, 0 for anti-clockwise) 
pi.set_PWM_dutycycle(STEP, 255 // 2)  # On-off half of the time

def spin(rotations):
    FREQ = 500 # Steps per second
    RESOLUTION = 200 # Steps per revolution
    waiting_time = (RESOLUTION / FREQ) * rotations

    pi.set_PWM_frequency(STEP, FREQ)  # 500 pulses per second
    sleep(waiting_time)
    pi.set_PWM_dutycycle(STEP, 0)  # PWM off


def exit_function(sig, frame):
    print("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
    pi.set_PWM_dutycycle(STEP, 0)  # PWM off
    pi.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, exit_function)
spin(1)
#signal.pause()
