import RPi.GPIO as GPIO



from time import sleep
GPIO.setmode(GPIO.BCM)


GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

pwm=GPIO.PWM(11, 100)

pwm.start(0)

GPIO.output(9, True)
GPIO.output(10, False)
pwm.ChangeDutyCycle(50)

GPIO.output(11, True)

sleep(2)

GPIO.output(11, False)