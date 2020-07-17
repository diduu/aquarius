#!/usr/bin/env python3


from time import sleep
from statistics import mean 
import time
import board
import busio
import adafruit_tcs34725
import RPi.GPIO as GPIO
import threading
import pigpio
import signal
import sys

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


def maprange(origin_range, target_range, value):
    (a1, a2), (b1, b2) = origin_range, target_range
    return b1 + ((value - a1) * (b2 - b1) / (a2 - a1))


def constrain(min_val, max_val, value):
    return max(min_val, min(max_val, value))


if __name__ == "__main__":
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_tcs34725.TCS34725(i2c)

    threads = []

    def exit_function(*args):
        print("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
        for thread in threads:
            thread.join() # Wait for motors to be done

        pi.stop()
        sys.exit(0)
    
    
    def sensor(rC, gC, bC):
        # rC, gC, bC = (23, 145), (23, 45), (16, 143)

        r, g, b = sensor.color_rgb_bytes
        print(f"Measured - R: {r}, G: {g}, B: {b}")

        updated = [
            constrain(0, 255, maprange(rC, (0, 255), r)),
            constrain(0, 255, maprange(gC, (0, 255), g)),
            constrain(0, 255, maprange(bC, (0, 255), b)),
        ]
        print("Calibrated - R: {}, G: {}, B: {}".format(*updated))
        return updates

    signal.signal(signal.SIGINT, exit_function)

    # PRIME
    # FLUSH
    # FILL
    # FLUSH
    # FILL TO 5 ML
    
    r, g, b = sensor.color_rgb_bytes
    rC, gC, bC = (0, r), (0, g), (0, b)

    while CONDITION:
        # ADD REAGENT
        avgR, avgG, avgB = [], [], []
        measures = 50
        for x in range(measures):
            new_val = sensor(rC, gC, bC)
            avgR += [new_val[0]]
            avgG += [new_val[1]]
            avgB += [new_val[2]]
            sleep(2/measures)

        avgR = sum(avgR) / len(avgR)
        avgG = sum(avgG) / len(avgG)
        avgB = sum(avgB) / len(avgB)
