import RPi.GPIO as GPIO
from time import sleep

pwm_pin = 12
inb_pin = 16
ina_pin = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.OUT)
GPIO.setup(inb_pin, GPIO.OUT)
GPIO.setup(ina_pin, GPIO.OUT)

pwm = GPIO.PWM(pwm_pin, 50)
pwm.start(0)

while(True):
    GPIO.output(inb_pin, False)
    GPIO.output(ina_pin, True)
    pwm.ChangeDutyCycle(25)
    sleep(5)
    pwm.stop()
    GPIO.cleanup()
#     GPIO.output(inb_pin, True)
#     GPIO.output(ina_pin, False)
#     pwm.ChangeDutyCycle(25)
#     sleep(5)
#     GPIO.cleanup()

