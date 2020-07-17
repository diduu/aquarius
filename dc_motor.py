import RPi.GPIO as GPIO
from time import sleep
from AMSpi import AMSpi

GPIO.setmode(GPIO.BOARD)

GPIO.setup(07, GPIO.OUT)
GPIO.setup(07, GPIO.OUT)
GPIO.setup(07, GPIO.OUT)

pwm=GPIO.PWM(07, 100)
pwm.start(0)

with AMSpi() as amspi:
	amspi.set_L293D_pins(5)
	amspi.run_dc_motor(amspi.DC_Motor_1)