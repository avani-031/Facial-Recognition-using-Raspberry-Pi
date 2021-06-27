import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

def led_on():
    print("LED on")
    GPIO.output(21,GPIO.HIGH)
    time.sleep(7)
def led_off():
    print("LED off")
    GPIO.output(21,GPIO.LOW)
    time.sleep(7)

def exit_led():
    print("Exiting, led off")
    GPIO.output(21,GPIO.LOW)
    time.sleep(3)