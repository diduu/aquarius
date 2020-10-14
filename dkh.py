#!/usr/bin/env python3

from picamera import PiCamera
import PIL
from PIL import Image
from time import sleep
from statistics import mean 
import time
import board
import busio
#import adafruit-tcs34725
import RPi.GPIO as GPIO
import threading
import pigpio
import signal
import sys
import csv
import datetime
from twilio.rest import Client


# Connect to pigpiod daemon
pi = pigpio.pi()
#camera = PiCamera()


#####TOP DC##### 
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
pwm=GPIO.PWM(4, 100)
pwm.start(0)
GPIO.output(2, True)
GPIO.output(3, False)


#####MIDDLE DC##### 
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
pwm2=GPIO.PWM(11, 100)
pwm2.start(0)
GPIO.output(9, True)
GPIO.output(10, False)


#####BOTTOM DC##### 
GPIO.setup(5, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
pwm3=GPIO.PWM(6, 100)
pwm3.start(0)
GPIO.output(5, True)
GPIO.output(12, False)

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


def top_dc():
    pwm.ChangeDutyCycle(100)
    GPIO.output(4, True)
    sleep(3)
    pwm.ChangeDutyCycle(0)
    GPIO.output(4, False)

def middle_dc():
    pwm2.ChangeDutyCycle(100)
    GPIO.output(11, True)
    sleep(1)
    pwm2.ChangeDutyCycle(0)
    GPIO.output(11, False)

def bottom_dc():
    pwm3.ChangeDutyCycle(100)
    GPIO.output(6, True)
    sleep(1)
    pwm3.ChangeDutyCycle(0)
    GPIO.output(6, False)


def output(dkh):
    now = datetime.datetime.now()
    a = [[now.strftime('%Y-%m-%d' + ' %H:%M:%S')], [dkh]]
    with open('results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(a)
    client = Client("", "")
    client.messages.create(to="+447905843784", 
                       from_="+12512573510", 
                       body="Your DKH was tested at: " + now.strftime('%Y-%m-%d' + ' %H:%M:%S\n' + "DKH Value: " + str(dkh)))


def maprange(origin_range, target_range, value):
    (a1, a2), (b1, b2) = origin_range, target_range
    return b1 + ((value - a1) * (b2 - b1) / (a2 - a1))


def constrain(min_val, max_val, value):
    return max(min_val, min(max_val, value))

#def reprime():


if __name__ == "__main__":
    correction_factor = 0.308
    XL = 342
    XR = 495
    YB = 351
    YT = 443
    pixels = (XR - XL) * (YT - YB)

    avgR, avgG, avgB = 0, 0, 0 

    threads = []

    def exit_function(*args):
        print("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
        for thread in threads:
            thread.join() # Wait for motors to be done

        pi.stop()
        sys.exit(0)


    #top_dc()
    #middle_dc()
    #bottom_dc()
    #spin(21, 20, 1, 57.677777778)
    #spin(21, 20, 0, 57.677777778)
    #spin(21, 20, 1, 57.677777778)
    #spin(21, 20, 0, 57.677777778)
    #spin(21, 20, 1, 57.677777778)
    spin(21, 20, 1, 57.677777778)
    spin(21, 20, 1, 2.5)
    spin(21, 20, 0, 2.5)
    
    '''
    print("Flush 1")
    spin(19, 20, 1, 70)

    print("Fill 1")
    spin(26, 20, 1, 58)
    
    dc_motor()
    
    print("Flush 2")
    spin(19, 20, 1, 70)

    
    print("Test Start")
    spin(26, 20, 1, 58)
    
    print("Adding Reagent")
    spin(21, 20, 1, 0.15)
    
    loop = True
    counter = 1

    while loop:
        spin(21, 20, 1, 0.15) 
        avgR, avgG, avgB = 0, 0, 0 
        counter += 1
        dc_motor()
        sleep(2)
        camera.start_preview(alpha=200)
        camera.capture('/home/pi/aquarius/images/image.jpg')
        camera.stop_preview()
        image = PIL.Image.open("/home/pi/aquarius/images/image.jpg")
        image_rgb = image.convert("RGB")
        for x in range(XL, XR):
            for y in range(YB, YT):
                rgb_pixel_value = image_rgb.getpixel((x, y))
                avgR += rgb_pixel_value[0]
                avgG += rgb_pixel_value[1]
                avgB += rgb_pixel_value[2]
        R = avgR / pixels
        G = avgG / pixels
        B = avgB / pixels
        print(str(counter) + ": " + str(R) + ", " + str(G) + ", " + str(B))
        if(counter < 5 or (R < B and G < B)):
            continue
        else:
            print("Test Finished")
            dkh = counter * correction_factor
            output(round(dkh, 2))
            loop = False
    
    '''    






