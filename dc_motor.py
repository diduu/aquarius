import RPi.GPIO as GPIO



from time import sleep
GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

pwm=GPIO.PWM(13, 100)
pwm.start(0)


GPIO.output(5, True)
GPIO.output(6, False)


pwm.ChangeDutyCycle(100)
GPIO.output(13, True)
sleep(20)
pwm.ChangeDutyCycle(0)
GPIO.output(13, False)