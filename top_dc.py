import RPi.GPIO as GPIO



from time import sleep
GPIO.setmode(GPIO.BCM)


GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

pwm=GPIO.PWM(4, 100)

pwm.start(0)

GPIO.output(2, True)
GPIO.output(3, False)
pwm.ChangeDutyCycle(100)

GPIO.output(4, True)

sleep(2)

GPIO.output(4, False)