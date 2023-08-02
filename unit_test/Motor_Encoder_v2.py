#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep
import sys
import signal

from Limit_Switch import Switch

class MotorDriver_Enc:
    def __init__(self):
        self.ANG = 12  # pin PWM
        self.DIG1 = 16  # pin DIR
        self.DIG2 = 20
        
        self.freq = 50
        self.max_speed = 10
        
        self.enc_a = 2
        self.enc_b = 3
        self.enc_z = 4
        
        self.pulse = 0
        self.pulse_state = 0
        
        self.ppr = 2488.2
        self.circumference = 68.5; #cm
    
    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.ANG, GPIO.OUT)              # set pin as output
        GPIO.setup(self.DIG1, GPIO.OUT)             # set pin as output
        GPIO.setup(self.DIG2, GPIO.OUT)
        self.p1 = GPIO.PWM(self.ANG, self.freq)                  # set pwm for M1
        self.p1.start(0)
        GPIO.setup(self.enc_a, GPIO.IN)
        GPIO.setup(self.enc_b, GPIO.IN)
        GPIO.setup(self.enc_z, GPIO.IN)
        
#     def signal_handler(self,sig, frame):
#         GPIO.cleanup()
#         sys.exit(0)

    def enc_a_callback(self,channel):
#         print("test")
        if GPIO.input(self.enc_b) == 0:
            if GPIO.input(self.enc_a) == 0:
                self.pulse-=1
            else:
                self.pulse+=1
#         print("pulse: ", self.pulse)
        cm = abs(((self.circumference / self.ppr) * self.pulse))
#         print(cm)
        sleep(0.1)
        return(cm)
    
    def Set_Zero(self):
        SW = Switch()
        self.setup_gpio()
        while not(SW):
            SW = Switch()
            GPIO.output(self.DIG1, GPIO.HIGH)
            GPIO.output(self.DIG2, GPIO.LOW)
            self.p1.ChangeDutyCycle(self.max_speed)
        self.pulse = 0
        self.p1.stop()
        GPIO.cleanup()
        
    def Run_Enc(self,bin_dist):
        self.Set_Zero()
        enc_read = 0.0
        delta_dist = enc_read - bin_dist
        
        while (delta_dist != 0):
            self.setup_gpio()
            if delta_dist <= 0:
                GPIO.output(self.DIG1, GPIO.LOW)
                GPIO.output(self.DIG2, GPIO.HIGH)
                self.p1.ChangeDutyCycle(self.max_speed)
            elif delta_dist >= 0:
                GPIO.output(self.DIG1, GPIO.HIGH)
                GPIO.output(self.DIG2, GPIO.LOW)
                self.p1.ChangeDutyCycle(self.max_speed)           
        
            enc_read = GPIO.add_event_detect(self.enc_a, GPIO.BOTH, callback=self.enc_a_callback, bouncetime=1)
            if enc_read == None:
                enc_read = 0
#             print(enc_read)
            delta_dist = enc_read - bin_dist
            self.p1.stop()
            print(delta_dist)
            GPIO.cleanup()
            delta_dist = input("Distance now")
#         return True
        
#             self.signal.signal(signal.SIGINT, signal_handler)
#             self.signal.pause()

if __name__ == '__main__':
    M = MotorDriver_Enc()
    M.Run_Enc(26)