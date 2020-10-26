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
from graph import showGraph


# Connect to pigpiod daemon
pi = pigpio.pi()



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

global total



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

def mixer(t=0.2):
    pwm.ChangeDutyCycle(100)
    GPIO.output(4, True)
    sleep(t)
    pwm.ChangeDutyCycle(0)
    GPIO.output(4, False)

def big_mixer():
    mixer(2)

def medium_mixer():
    mixer(1)

def flush():
    pwm2.ChangeDutyCycle(100)
    GPIO.output(11, True)
    sleep(5)
    pwm2.ChangeDutyCycle(0)
    GPIO.output(11, False)

def fill():
    pwm3.ChangeDutyCycle(100)
    GPIO.output(6, True)
    sleep(3)
    pwm3.ChangeDutyCycle(0)
    GPIO.output(6, False)


def camera():
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
    return (R, G, B)


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

def test():
    loop = True
    loop2 = False
    loop3 = False
    loop4 = False
    counter1 = 0
    while loop:
        spin(21, 20, 0, 4.615) 
        mixer()
        avgR, avgG, avgB = 0, 0, 0 
        counter1 += 100
        #mixer()
        sleep(0.2)
        R, G, B = camera()
        # writer.writerow((R, G, B))
        print(f"{counter1}: {R}, {G}, {B}")
        if(B > G and R > 20):
            loop = False
            loop2 = True
        elif(B > G and R < 20):
            loop = False
            loop3 = True
        
    while loop2:
        spin(21, 20, 0, 2.3075) 
        mixer()
        avgR, avgG, avgB = 0, 0, 0 
        counter1 += 50
        #mixer1)
        sleep(0.2)
        R, G, B = camera()
        # writer.writerow((R, G, B))
        print(f"{counter1}: {R}, {G}, {B}")
        if(B < G or R < 20):
            loop2 = False
            loop3 = True

    while loop3:
        spin(21, 20, 0, 1.15375) 
        mixer()
        avgR, avgG, avgB = 0, 0, 0 
        counter1 += 25
        #mixer1)
        sleep(0.2)
        R, G, B = camera()
        # writer.writerow((R, G, B))
        print(f"{counter1}: {R}, {G}, {B}")
        if(B < 105 or R > 20):
            loop3 = False
            loop4 = True
    
   
    while loop4:
        spin(21, 20, 0, 0.04615) 
        mixer()
        avgR, avgG, avgB = 0, 0, 0 
        counter1 += 1
        #mixer1)
        sleep(0.2)
        R, G, B = camera()
        writer.writerow((R, G, B))
        print(f"{counter1}: {R}, {G}, {B}")
        if(B < G and R > 20):
            dkh1 = ((counter1 * 0.001) * 27.808656036)
            print(dkh1)
            reprime = ((counter1 * 0.04615) + 2)
            spin(21, 20, 1, reprime)
            # row_count = len(list(reader))
            results.close()
            loop4 = False      

'''
def test2():
    loop5 = True
    loop6 = False
    loop7 = False
    loop8 = False
    counter2 = 0
    while loop5:
        spin(21, 20, 0, 4.615) 
        mixer()
        avgR, avgG, avgB = 0, 0, 0 
        counter2 += 100
        #mixer()
        sleep(0.2)
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
        RGB = (R, G, B)
        writer2.writerow(RGB)
        print(str(counter2) + ": " + str(R) + ", " + str(G) + ", " + str(B))
        if(G > B):
            continue
        elif(B > G and R > 20):
            loop5 = False
            loop6 = True
        elif(B > G and R < 20):
            loop5 = False
            loop7 = True
        
    while loop6:
        spin(21, 20, 0, 2.3075) 
        mixer()
        avgR, avgG, avgB = 0, 0, 0 
        counter2 += 50
        #mixer1)
        sleep(0.2)
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
        RGB = (R, G, B)
        writer2.writerow(RGB)
        print(str(counter2) + ": " + str(R) + ", " + str(G) + ", " + str(B))
        if(B > G and R > 20):
            continue
        else:
            loop6 = False
            loop7 = True

    while loop7:
        spin(21, 20, 0, 1.15375) 
        mixer()
        avgR, avgG, avgB = 0, 0, 0 
        counter2 += 25
        #mixer1)
        sleep(0.2)
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
        RGB = (R, G, B)
        writer2.writerow(RGB)
        print(str(counter2) + ": " + str(R) + ", " + str(G) + ", " + str(B))
        if(B > 105 and R < 20):
            continue
        else:
            loop7 = False
            loop8 = True
    
    while loop8:
        spin(21, 20, 0, 0.04615) 
        mixer()
        avgR, avgG, avgB = 0, 0, 0 
        counter2 += 1
        #mixer1)
        sleep(0.2)
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
        RGB = (R, G, B)
        writer2.writerow(RGB)
        print(str(counter2) + ": " + str(R) + ", " + str(G) + ", " + str(B))
        if(B > G and R < 20):
            continue
        elif(B < G and R > 20):
            dkh2 = ((counter2 * 0.001) * 27.808656036)
            print(dkh2)
            reprime = ((counter2 * 0.04615) + 2)
            spin(21, 20, 1, reprime)
            row_count2 = len(list(reader2))
            results2.close()
            loop8 = False      
'''

if __name__ == "__main__":
    correction_factor = 0.308
    XL = 610
    XR = 650
    YB = 200
    YT = 230
    pixels = (XR - XL) * (YT - YB)
    dkh1 = 0
    dkh2 = 0

    camera = PiCamera()

    new_name = f"{datetime.timestamp(datetime.now())}.csv"
    results = open(new_name, 'w', newline='') 
    writer = csv.writer(results)
    test()
    showGraph(new_name)
    # reader = csv.reader(results)

    #results2 = open('results2.csv','r+', newline='') 
    #writer2 = csv.writer(results2)
    #reader2 = csv.reader(results2)


    avgR, avgG, avgB = 0, 0, 0 

    threads = []

    def exit_function(*args):
        print("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
        for thread in threads:
            thread.join() # Wait for motors to be done

        pi.stop()
        sys.exit(0)


    #top_dc()
    #flush()
    #fill()
    #for x in range(50):
    #    mixer()
    #    sleep(0.1)
    #flush()
    #spin(21, 20, 0, 1)

    #spin(21, 20, 0, 5)
    #spin(21, 20, 1, 57.677777778)
    #spin(21, 20, 0, 57.677777778)
    #spin(21, 20, 1, 57.677777778)
    #spin(21, 20, 1, 57.677777778)
    #
    #spin(21, 20, 1, 2)
    #spin(21, 20, 0, 1)

    
    #spin(21, 20, 1, 1)
    #spin(21, 20, 0, 1)
    #spin(21, 20, 1, 1)
    #spin(21, 20, 0, 1)
    #spin(21, 20, 1, 1)
    #spin(21, 20, 0, 46.15)
    #spin(21, 20, 0, 46.15)

    #spin(21, 20, 1, 6.615)
    #spin(21, 20, 0, 2)
    #
    #spin(21, 20, 1, 5) ]
    
    #spin(21, 20, 0, 0.5)

    #flush()
    #print("Adding Reagent")
    #spin(21, 20, 0, 4.615)

    

    #spin(21, 20, 1, 23.5059)
    #fill()

    spin(21, 20, 0, 2)

    
    
    #flush()
    #spin(21, 20, 1, 2)
    #mixer()
    '''
    spin(21, 20, 0, 2)

    
    print("Flush 1")
    flush()
    print("Fill 1")
    fill()
    
    mixer()
    print("Flush 2")
    flush()
    print("Fill 2")
    fill()
    mixer()
    print("Flush 3")
    flush()
    print("Test Start")
    fill()

    test()


    
    #row_count = len(list(reader))
    #spin(21, 20, 1, 23.36745)
    spin(21, 20, 0, 2)

    #counter = 0

    #spin(21, 20, 0, 2)
    print("Flush 1")
    flush()
    print("Fill 1")
    fill()
    mixer()
    print("Flush 2")
    flush()
    print("Fill 2")
    fill()
    mixer()
    print("Flush 3")
    flush()
    print("Test Start")
    fill()
    
    test2()
    print(str((row_count +  row_count2) / 2))
    '''
    
    
    

    
    
           
