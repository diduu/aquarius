#!/usr/bin/env python3

from time import sleep
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

def calibrate():
    r = g = b = 0
    minR = minG = minB = 255
    maxR = maxG = maxB = 0
    minThreshold = 10
    state = 0  # 0: black, 1: white, 2: done

    def button_press():
        if state == 0:
            minR, minG, minB = r, g, b
            print("White...")
            state = 1
        elif state == 1:
            maxR, maxG, maxB = r, g, b
            print("Done")
            state = 2


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

    signal.signal(signal.SIGINT, exit_function)

    # One after the other
    #spin(26, 20, 0, 50)
    #sleep(1)
    #spin(19, 20, 0, 0.06)
    #sleep(1)
    #spin(21, 20, 1, 60) #21 is fill

    rC, gC, bC = (0, 54), (0, 54), (0, 56)

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
