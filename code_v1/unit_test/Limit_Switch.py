# coding=utf-8
 
import RPi.GPIO as GPIO
import time

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    count = 0

def Switch():
    setup_gpio()
    if GPIO.input(25) == GPIO.HIGH:
        print("Now motor is in zero position")
        GPIO.cleanup()
        return True
    else:
        return False
    
# while(True):
# #     print(GPIO.input(25))
#     if GPIO.input(25) == GPIO.HIGH:
#         print("Goodbye!")
#         break
#     else:
#         count = count + 1
#         print("Nothing!!!!!!!!!!  " , count)
#     time.sleep(0.01)
    
 
