#!/usr/bin/env python3

import pigpio
import signal
import sys
from time import sleep
import threading


def maprange(origin_range, target_range, value):
    (a1, a2), (b1, b2) = origin_range, target_range
    return b1 + ((value - a1) * (b2 - b1) / (a2 - a1))

def constrain(min_val, max_val, value):
    return max(min_val, min(max_val, value))

def sensor():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_tcs34725.TCS34725(i2c)

    rC, gC, bC = (23, 145), (23, 45), (16, 143)

    while True:
        r, g, b = sensor.color_rgb_bytes
        print(f"Measured - R: {r}, G: {g}, B: {b}")

        updated = [
            constrain(0, 255, maprange(rC, (0, 255), r)),
            constrain(0, 255, maprange(gC, (0, 255), g)),
            constrain(0, 255, maprange(bC, (0, 255), b)),
        ]
        print("Calibrated - R: {}, G: {}, B: {}".format(*updated))
        sleep(1)

# Connect to pigpiod daemon
pi = pigpio.pi()

def spin(dir, step):
    # Set up pins as an output
    pi.set_mode(dir, pigpio.OUTPUT)
    pi.set_mode(step, pigpio.OUTPUT)

    # Set direction (1 for clockwise, 0 for anti-clockwise)
    pi.write(dir, 1)

    # Set duty cycle and frequency
    pi.set_PWM_dutycycle(step, 255 // 2)  # On-off half of the time
    pi.set_PWM_frequency(step, 500)  # 500 pulses per second


if __name__ == "__main__":
    DIR = 20  # Direction GPIO Pin
    STEP = 21  # Step GPIO Pin
    spin(DIR, STEP)

    def exit_function(sig, frame):
        print("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
        pi.set_PWM_dutycycle(STEP, 0)  # PWM off
        pi.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_function)
    sensor()
