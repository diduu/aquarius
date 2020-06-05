#!/usr/bin/env python3

from time import sleep
import board
import busio
import adafruit_tcs34725
import RPi.GPIO as GPIO


def spin(seq, control):
    GPIO.setmode(GPIO.BCM)
    for pin in control:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    for _ in range(512):
        for halfstep in seq:
            for i, pin in enumerate(control):
                GPIO.output(pin, halfstep[i])
            sleep(0.001)
    GPIO.cleanup()


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
    seq = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_tcs34725.TCS34725(i2c)

    spin(seq, [17, 18, 27, 22])
    spin(seq, [23, 24, 10, 9])  # spin2

    calibration = (0, 255)

    while True:
        r, g, b = sensor.color_rgb_bytes
        print(f"Measured - R: {r}, G: {g}, B: {b}")

        if calibration:
            updated = [
                constrain(0, 255, maprange((0, 255), calibration, color))
                for color in (r, g, b)
            ]
            print("Modified - R: {}, G: {}, B: {}".format(*updated))

        print(sensor.color_raw)
        sleep(1)
