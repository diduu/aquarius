#!/usr/bin/env python3

import pigpio
import signal
import sys
import threading
from time import sleep

# Connect to pigpiod daemon
pi = pigpio.pi()

def spin(STEP, DIR, direction, rotations):
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

    while True:
        command = input('> ').lower().split(' ')
        
        if command[0] in ['q', 'quit']:
            exit_function()
        elif command[0] == 'spin' and len(command) == 5:
            args = [int(x) for x in command[1:]]
            thread = threading.Thread(target=spin, args=tuple(args))
            threads = threads + [thread]
            thread.start()
        else:
            print('Wrong command, usage:'
            print('spin <motor_pin> <direction_pin> <direction> <number_of_rotations>')
