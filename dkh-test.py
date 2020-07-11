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
    
    
    output = []
    def sense():
        readings = []
        t_end = time.time() + 1
        while time.time() < t_end:
            updated = [
                constrain(0, 255, maprange(rC, (0, 255), r)),
                constrain(0, 255, maprange(gC, (0, 255), g)),
                constrain(0, 255, maprange(bC, (0, 255), b)),
            ]
            #print("Calibrated - R: {}, G: {}, B: {}".format(*updated))
            sleep(0.001)
            readings.append(updated)

        red = [i[0] for i in readings]
        green = [i[1] for i in readings]
        blue = [i[2] for i in readings]
        #print(red, green, blue)
        output.append([mean(red), mean(green), mean(blue)])

    signal.signal(signal.SIGINT, exit_function)


    print("Flush 1")
    spin(19, 20, 1, 70)
    
    print("fill 1")
    spin(21, 20, 1, 58)

    print("flush 2")
    spin(19, 20, 1, 70)


    print("test start")
    spin(21, 20, 1, 29)
    
    
    #sleep(5)
    
    r, g, b = sensor.color_rgb_bytes    
    rC, gC, bC = (0, r), (0, g), (0, b)
    
    spin(26, 20, 1, 0.075)
    loop = True
    counter = 1

    while loop:
        sleep(1)
        sense()
        if(output[0][0] < output[0][2]):
            output.pop(0)
            spin(26, 20, 1, 0.075)
            counter += 1
            print(str(counter) + ": " + str(updated))
            sleep(1)
        elif(output[0][0] > output[0][2]):
            print("test end")
            loop = False
            print(counter * 0.25)
    
    



