import RPi.GPIO as GPIO
import time
import sys
import signal

from Ultrasonic import distance
from Door_Motor import MotorDriver

from Motor_Encoder_v2 import MotorDriver_Enc
from Servo_v4 import setAngle

class Control:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.bin_dist = {"plastic" : 0,
                         "metal" : 26,
                         "glass" : 52,
                         "other" : 78} #length of bin = 26 cm

    def State1(self,min_hand_dist, max_hand_dist, hand_check):
        Door_MD = MotorDriver()
    
        while(True):
            hand_dist = distance(17,27)
            hand_loop = 0
        
            if hand_dist <= min_hand_dist or hand_dist >= max_hand_dist:
                print("---------------start--------------")
                Door_MD.run_motor_driver(True)
                while hand_loop <= hand_check:
                    hand_dist = distance(17,27)
                    if hand_dist <= min_hand_dist or hand_dist >= max_hand_dist:
                        hand_loop = 0
                        print("Check Hand again")
                    else:
                        hand_loop = hand_loop + 1
                        print(hand_loop , "   Still see the hand   " , hand_dist)
                print("!!!!!!!!!!!!!No hand !!!!!!!!!!!!!!!!")
                Door_MD.run_motor_driver(False)
                return(True)
            
            else:
                print (hand_dist)
        GPIO.cleanup()
    
    def Bin_Dist_Check(self, max_bin_dist):
        hand_dist = distance(17,27) #for testing
        bin1_dist = distance(10,22)
#         bin2_dist = distance(11,9)
#         bin3_dist = distance(6,5)
#         bin4_dist = distance(21,26)

        if ((hand_dist <= max_bin_dist) or (bin1_dist <= max_bin_dist)):
            #or (bin2_dist <= max_bin_dist) or (bin3_dist <= max_bin_dist) or (bin4_dist <= max_bin_dist)):
            print("Error : Bin is full !!!")
            return True #bin is full
        else:
            return False
    
    def State2(self, trash_type):
        MD_E = MotorDriver_Enc()
        length = self.bin_dist[trash_type] #cm
        print("Move length is : ", length, "cm")
        run_enc = MD_E.Run_Enc(length)
        setAngle(90)
        sleep(1)
        setAngle(0)
        sleep(1)
        MD_E.Set_Zero()
        return True

# if __name__ == '__main__':
#     Control.State1(9,150,30)
#     Control.State2("test")

