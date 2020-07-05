#!/usr/bin/env python3

import pigpio
import signal
import sys
import threading
from time import sleep

# Connect to pigpiod daemon
pi = pigpio.pi()

def spin(STEP, DIR, direction, rotations): # Rotations doesn't need to be an int
    # Set up pins as an output
    pi.set_mode(DIR, pigpio.OUTPUT)
    pi.set_mode(STEP, pigpio.OUTPUT)

    pi.write(DIR, direction) # Set direction (1 for clockwise, 0 for anti-clockwise) 
    pi.set_PWM_dutycycle(STEP, 255 // 2)  # On-off half of the time

    FREQ = 500 # Steps per second
    RESOLUTION = 200 # Steps per revolution
    waiting_time = (RESOLUTION / FREQ) * rotations

    pi.set_PWM_frequency(STEP, FREQ)  # 500 pulses per second
    sleep(waiting_time)
    pi.set_PWM_dutycycle(STEP, 0)  # PWM off

if __name__ == "__main__":
    threads = []

    def exit_function(*args):
        print("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
        for thread in threads:
            thread.join() # Wait for motors to be done

        pi.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_function)

    # One after the other
    # spin(STEP, DIR, direction, rotations)
    # spin(STEP, DIR, direction, rotations)
    # spin(STEP, DIR, direction, rotations)

    # Two at the same time
    # thread = threading.Thread(target=spin, args=(STEP, DIR, direction, rotations))
    # threads = threads + [thread]
    # thread.start()
    # thread = threading.Thread(target=spin, args=(STEP, DIR, direction, rotations))
    # threads = threads + [thread]
    # thread.start()
    # You can add a 3rd spin here and it will run at the same time as the otehr 2

    # Wait for all 3 of them to finish
    # for thread in threads:
    #         thread.join()

    # You can repeat any of the above however many times you need
