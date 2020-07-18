from time import sleep
import board
import busio
from adafruit_as726x import AS726x_I2C
import RPi.GPIO as GPIO
import threading



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
	sensor = Adafruit_AS726x_I2C(i2c)



    while True:
        r, g, b = sensor.color_rgb_bytes
        print(f"Measured - R: {r}, G: {g}, B: {b}")

        #updated = [
        #    constrain(0, 255, maprange(rC, (0, 255), r)),
        #    constrain(0, 255, maprange(gC, (0, 255), g)),
        #    constrain(0, 255, maprange(bC, (0, 255), b)),
        #]
        #print("Calibrated - R: {}, G: {}, B: {}".format(*updated))


        print(sensor.color_raw)
        sleep(1)

