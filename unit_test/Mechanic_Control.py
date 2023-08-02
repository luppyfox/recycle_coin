import RPi.GPIO as GPIO
import time
import sys
import signal

from Ultrasonic import distance
min_distance = 9
max_distance = 150
hand_check = 50

from Door_Motor import MotorDriver

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

if __name__ == '__main__':
    MD = MotorDriver()
    dist = distance()
    
    while(True):
        dist = distance()
        hand_loop = 0
        if dist <= min_distance or dist >= max_distance:
            print("---------------start--------------")
            while hand_loop <= hand_check:
                dist = distance()
                if dist <= min_distance or dist >= max_distance:
                    hand_loop = 0
                    print("redo", hand_loop)
                else:
                    hand_loop = hand_loop + 1
                    print(hand_loop , "   handddd   " , dist)
            print("!!!!!!!!!!!!!No hand !!!!!!!!!!!!!!!!")
            MD.run_motor_driver(True)
            
            

        else:
            print (dist)
    GPIO.cleanup()
