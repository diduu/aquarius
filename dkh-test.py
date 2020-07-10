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
    #spin(26, 20, 0, 50) #flush
    #sleep(1)
    #spin(19, 20, 0, 0.15) #reagent
    #sleep(1)
    #spin(21, 20, 1, 60) #fill
    
    #spin(21, 20, 1, 58)
    #spin(26, 20, 0, 70)
    #spin(19, 20, 1, 20)

    spin(26, 20, 0, 70)
    spin(21, 20, 1, 58)
    spin(26, 20, 0, 100)
    spin(21, 20, 1, 29)
    #spin(26, 20, 0, 20)
    spin(19, 20, 0, 0.15)
    sleep(5)

    rC, gC, bC = (0, 37), (0, 44), (0, 53)

    loop = True
    counter = 1
    
    while loop:
        r, g, b = sensor.color_rgb_bytes

        updated = [
            constrain(0, 255, maprange(rC, (0, 255), r)),
            constrain(0, 255, maprange(gC, (0, 255), g)),
            constrain(0, 255, maprange(bC, (0, 255), b)),
        ]

        if(updated[0] < updated[2]):
            spin(19, 20, 0, 0.15)
            counter += 1
            print(str(counter) + ": " + str(updated))
            sleep(5)
        elif(updated[0] > updated[2]):
            print("test end")
            loop = False
            print(counter)
            print(counter * 0.5)
    
            



