import RPi.GPIO as GPIO
from time import sleep
import sys
import signal

from Mechanic_Control import Control
from Camera_v2 import Cap_Img

img_count = 0
trash_type = ""
trash_data = {"plastic" : 0,     #for testing
              "metal" : 0,
              "glass" : 0,
              "other" : 0}

min_hand_dist = 9
max_hand_dist = 150
hand_check_loop = 30

max_bin_dist = 8 #bin is full distance

if __name__ == '__main__':
    C = Control()
    while True:
        bin_full = C.Bin_Dist_Check(max_bin_dist)
        while not(bin_full):
            MC_St1 = C.State1(min_hand_dist,max_hand_dist,hand_check_loop)
            print("Mechanic Control State 1 = ", MC_St1)
            sleep(0.5)
            if MC_St1 == True:
                Cap_Img(img_count)
                img_count = img_count + 1
                trash_type = input("Enter the type of trash : ")
                if trash_type != "":
                    trash_data[trash_type] = trash_data[trash_type] + 1      #for testing
                    print("The type of trash is ", trash_type, " Count : ",trash_data[trash_type])
                    C.State2(trash_type)
            
            bin_full = C.Bin_Dist_Check(max_bin_dist)

#     while(True):
#         MC_St1 = C.State1(min_hand_dist,max_hand_dist,hand_check_loop)
#         print("Mechanic Control State 1 = ", MC_St1)
#         sleep(0.5)
#         if MC_St1 == True:
#             Cap_Img(img_count)
#             img_count = img_count + 1
#             trash_type = input("Enter the type of trash : ")
#             if trash_type != "":
#                 trash_data[trash_type] = trash_data[trash_type] + 1      #for testing
#                 print("The type of trash is ",trash_data[trash_type])
                
    