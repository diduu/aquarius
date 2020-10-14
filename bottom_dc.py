import RPi.GPIO as GPIO



from time import sleep
GPIO.setmode(GPIO.BCM)


GPIO.setup(5, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
pwm=GPIO.PWM(6, 100)
pwm.start(0)

GPIO.output(5, True)
GPIO.output(12, False)
pwm.ChangeDutyCycle(100)
GPIO.output(6, True)
sleep(2)
pwm.ChangeDutyCycle(0)
GPIO.output(6, False)