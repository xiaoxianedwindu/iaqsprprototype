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
spinTime = 0.0001

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
 
x = 0
y = 0
c = 0
coordStatus = 0 
goStatus = 1


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
        reverseLeft.value = 0.6
        forwardRight.value = 0.6
        reverseRight.value = 0
 
def spinRight():
        print("spinRight")
        forwardLeft.value = 0.7
        reverseLeft.value = 0
        forwardRight.value = 0
        reverseRight.value = 0.7
        
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
    if (distance_0 < 30):
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
    #print(distance_0)
    global x, y, goStatus
    printInfo()
    if (distance_0 < 40):
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
            goL()
        else:
            spinRight()
            time.sleep(spinTime)
            #print("Right is clear")
            goR()
        time.sleep(1.25)
    else:
        forwardDrive()
        #print("Status = " + str(goStatus))
        coord(goStatus)
        flag = 0
        
def goL():
    global goStatus
    if (goStatus == 1):
        goStatus = 3
    elif (goStatus == 2):
        goStatus = 4
    elif (goStatus == 3):
        goStatus = 2
    elif (goStatus == 4):
        goStatus = 1
    else:
        print("goL oops")
        
def goR():
    global goStatus
    if (goStatus == 1):
        goStatus = 4
    elif (goStatus == 2):
        goStatus = 3
    elif (goStatus == 3):
        goStatus = 1
    elif (goStatus == 4):
        goStatus = 2
    else:
        print("goR oops")
        
def coord(coordStatus):
    global x, y
    if (coordStatus == 1):
        x += 1
    elif (coordStatus == 2):
        x -= 1
    elif (coordStatus == 3):
        y += 1
    elif(coordStatus == 4):
        y -= 1
    else:
        print("oops")

def sensor_input():
    global pm25_current
    pm25_1 = int(ser.readline())
    #print(pm25_1)
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

def printInfo():
    global x, y, goStatus, pm25_current
    print(x, y, goStatus, pm25_current)
              
def main():
        checkForwardDrive()
        sensor_input()
        #switchcheck()
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

