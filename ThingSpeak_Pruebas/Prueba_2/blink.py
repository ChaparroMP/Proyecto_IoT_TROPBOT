import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

ledPin = 11 #GPIO 17

# GPIO Configuration as a output and assigment of PIN
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)


GPIO.output(ledPin, GPIO.HIGH)
time.sleep(1)
GPIO.output(ledPin, GPIO.LOW)
time.sleep(1)

print("se ejecuta archivo blink.py")
    
GPIO.cleanup()