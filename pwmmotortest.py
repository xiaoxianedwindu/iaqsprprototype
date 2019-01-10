#!/usr/bin/env python3
 
"""
File: skidsteer_four_pwm_test.py
 
This code will test Raspberry Pi GPIO PWM on four GPIO
pins. The code test ran with L298N H-Bridge driver module connected.
 
Website:	www.bluetin.io
Date:		27/11/2017
"""
 
__author__ = "Mark Heywood"
__version__ = "0.1.0"
__license__ = "MIT"
 
from gpiozero import PWMOutputDevice
from time import sleep
 
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
 
def SpinRight():
        print("SpinRight")
        forwardLeft.value = 1.0
        reverseLeft.value = 0
        forwardRight.value = 0
        reverseRight.value = 1.0
 
def forwardTurnLeft():
        print("fowardTurnLeft")
        forwardLeft.value = 0.8
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
 
def main():
        allStop()
        '''
        forwardDrive()
        sleep(5)
        reverseDrive()
        sleep(5)
        '''
        spinLeft()
        sleep(2.5)
        '''
        SpinRight()
        sleep(2.5)
        forwardTurnLeft()
        sleep(5)
        forwardTurnRight()
        sleep(5)
        reverseTurnLeft()
        sleep(5)
        reverseTurnRight()
        sleep(5)
        allStop()
        '''
 
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()