import RPi.GPIO as GPIO
from time import sleep

class MotorDriver():
    def __init__(self):
        self.ANG = 12  # pin PWM
        self.DIG1 = 16  # pin DIR
        self.DIG2 = 20
        self.freq = 50
        self.max_speed = 10
    
    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.ANG, GPIO.OUT)              # set pin as output
        GPIO.setup(self.DIG1, GPIO.OUT)             # set pin as output
        GPIO.setup(self.DIG2, GPIO.OUT)
        self.p1 = GPIO.PWM(self.ANG, self.freq)                  # set pwm for M1
        self.p1.start(0)
    
    def run_motor_driver(self,on):
        self.setup_gpio()
        
        if on == True:
            GPIO.output(self.DIG1, GPIO.LOW)
            GPIO.output(self.DIG2, GPIO.HIGH)
            self.p1.ChangeDutyCycle(self.max_speed)
            sleep(2)
        elif on == False:
            GPIO.output(self.DIG1, GPIO.HIGH)
            GPIO.output(self.DIG2, GPIO.LOW)
            self.p1.ChangeDutyCycle(self.max_speed)
            sleep(2)
        else:
            GPIO.output(self.DIG1, GPIO.LOW)
            GPIO.output(self.DIG2, GPIO.LOW)
            self.p1.ChangeDutyCycle(0)
            sleep(2)
            
        self.p1.stop()
#         GPIO.cleanup()

if __name__ == '__main__':
    MD_object = MotorDriver()
    MD_object.run_motor_driver(True)