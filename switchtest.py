import RPi.GPIO as gpio
import sys
import serial

from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
import time

SWITCH_PIN = 4
gpio.setup(SWITCH_PIN, gpio.OUT)

def switchon():
    gpio.output(SWITCH_PIN, gpio.HIGH)
    
def switchoff():
    gpio.output(SWITCH_PIN, gpio.LOW)
              
try:
    while True:
        switchoff()
        time.sleep(10)
        switchon()
        time.sleep(5)
        switchoff()
              
        
except KeyboardInterrupt:
    gpio.cleanup