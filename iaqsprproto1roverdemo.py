import RPi.GPIO as gpio
import sys
import serial

from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
import time

SWITCH_PIN = 4
MOTOR_PIN = 2
GPIO_TRIGGER = 23
GPIO_ECHO = 24
gpio.setup(MOTOR_PIN,gpio.OUT)
pwm_motor=gpio.PWM(MOTOR_PIN,50)
pwm_motor.start(7.5)
gpio.setup(GPIO_TRIGGER,gpio.OUT)
gpio.setup(GPIO_ECHO,gpio.IN)
gpio.setup(SWITCH_PIN, gpio.OUT)
spinTime = 0.025

ser = serial.Serial('/dev/ttyUSB0', 9600)

pm25_current = 0
 
#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
PWM_FORWARD_LEFT_PIN = 12	# IN1 - Forward Drive
PWM_REVERSE_LEFT_PIN = 16	# IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_FORWARD_RIGHT_PIN = 20	# IN1 - Forward Drive
PWM_REVERSE_RIGHT_PIN = 21	# IN2 - Reverse Drive
 
# Initialise objects for H-Bridge PWM pins
# Set initial duty cycle to 0 and frequency to 1000
forwardLeft = PWMOutputDevice(PWM_FORWARD_LEFT_PIN, True, 0, 1000)
reverseLeft = PWMOutputDevice(PWM_REVERSE_LEFT_PIN, True, 0, 1000)
 
forwardRight = PWMOutputDevice(PWM_FORWARD_RIGHT_PIN, True, 0, 1000)
reverseRight = PWMOutputDevice(PWM_REVERSE_RIGHT_PIN, True, 0, 1000)
 
 
def allStop():
        print("allStop")
        forwardLeft.value = 0
        reverseLeft.value = 0
        forwardRight.value = 0
        reverseRight.value = 0
 
def forwardDrive():
        print("forwardDrive")
        forwardLeft.value = 1.0
        reverseLeft.value = 0
        forwardRight.value = 1.0
        reverseRight.value = 0


def reverseDrive():
        print("reverseDrive")
        forwardLeft.value = 0
        reverseLeft.value = 1.0
        forwardRight.value = 0
        reverseRight.value = 1.0
 
def spinLeft():
        print("spinLeft")
        forwardLeft.value = 0
        reverseLeft.value = 1.0
        forwardRight.value = 1.0
        reverseRight.value = 0
 
def spinRight():
        print("spinRight")
        forwardLeft.value = 1.0
        reverseLeft.value = 0
        forwardRight.value = 0
        reverseRight.value = 1.0
 
def forwardTurnLeft():
        print("fowardTurnLeft")
        forwardLeft.value = 0.5
        reverseLeft.value = 0
        forwardRight.value = 1
        reverseRight.value = 0
 
def forwardTurnRight():
        print("forwardTurnRight")
        forwardLeft.value = 1
        reverseLeft.value = 0
        forwardRight.value = 0.5
        reverseRight.value = 0
 
def reverseTurnLeft():
        print("reverseTurnLeft")
        forwardLeft.value = 0
        reverseLeft.value = 0.5
        forwardRight.value = 0
        reverseRight.value = 1
 
def reverseTurnRight():
        print("reverseTurnRight")
        forwardLeft.value = 0
        reverseLeft.value = 1
        forwardRight.value = 0
        reverseRight.value = 0.5
        
def distance():
    gpio.output(23, False)
    time.sleep(0.5)
    gpio.output(23, True)
    time.sleep(0.00001)
    gpio.output(23, False)
    start = time.time()
    while gpio.input(24) == 0:
        start = time.time()
    while gpio.input(24) == 1:
        stop = time.time()
    elapsed = stop - start
    distance = elapsed * 34000
    distance = distance / 2
    return distance

def dist_check():
    distance_0 = distance()
    if (distance_0 < 20):
        pwm_motor.ChangeDutyCycle(2.5)
        time.sleep(0.5)
        pwm_motor.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        pwm_motor.ChangeDutyCycle(7.5)
    distance_0 = distance()
    print(distance_0)

def checkForwardDrive():
    flag = 0
    distance_0 = distance()
    print(distance_0)
    if (distance_0 < 20):
        allStop()
        pwm_motor.ChangeDutyCycle(2.5)
        time.sleep(0.75)
        distance_r = distance()
        print(distance_r)
        pwm_motor.ChangeDutyCycle(12.5)
        time.sleep(0.75)
        distance_l = distance()
        print(distance_l)
        pwm_motor.ChangeDutyCycle(7.5)

        allStop()
        if (distance_r < distance_l):
            spinLeft()
            time.sleep(spinTime)
            #print("Yo, left is clear")
        else:
            spinRight()
            time.sleep(spinTime)
            #print("Right is clear")
        time.sleep(1)
    else:
        forwardDrive()
        flag = 0

def sensor_input():
    pm25_1 = int(ser.readline())
    print(pm25_1)
    pm25_current = pm25_1
    if (pm25_1 > 30):
        switchon()
        time.sleep(2)
    else:
        switchoff()
    '''
    pm25_2 = int(ser.readline())
    pm25_3 = int(ser.readline())
    pm25_4 = int(ser.readline())
    pm25_5 = int(ser.readline())
    pm25_current = (pm25_1 + pm25_2 + pm25_3 + pm25_4 + pm25_5)/5
    print("Current PM2.5: " + str(pm25_current))
    '''

def switchon():
    gpio.output(SWITCH_PIN, gpio.HIGH)
    
def switchoff():
    gpio.output(SWITCH_PIN, gpio.LOW)
    
def switchcheck():
    print(pm25_1)
    if (pm25_current > 2):
        switchon()
        time.sleep(5)
    else:
        switchoff()
              
def main():
        #checkForwardDrive()
        #sensor_input()
        #switchcheck()
        forwardDrive()
        time.sleep(5)
        spinRight()
        time.sleep(3)
        fowardDrive()
        time.sleep(3)
        spinRight()
        time.sleep(2)
        allStop()
        time.sleep(10)
        '''
        reverseDrive()
        time.sleep(5)
        spinLeft()
        time.sleep(5)
        SpinRight()
        time.sleep(5)
        forwardTurnLeft()
        time.sleep(5)
        forwardTurnRight()
        time.sleep(5)
        reverseTurnLeft()
        time.sleep(5)
        reverseTurnRight()
        time.sleep(5)
        '''
        
try:
    while True:
        main()
        
except KeyboardInterrupt:
    gpio.cleanup()

