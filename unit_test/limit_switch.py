# coding=utf-8
 
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
count = 0

while(True):
#     print(GPIO.input(25))
    if GPIO.input(25) == GPIO.HIGH:
        print("Goodbye!")
        break
    else:
        count = count + 1
        print("Nothing!!!!!!!!!!  " , count)
    time.sleep(0.01)
    
 
