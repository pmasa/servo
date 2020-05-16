import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

relay_pin = 17 
servo1_pin = 6
servo2_pin = 5
PIR_SENSOR = 23

GPIO.setup(PIR_SENSOR, GPIO.IN)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
GPIO.setup(relay_pin, GPIO.OUT)

# Create PWM channel on the servo pin with a frequency of 50Hz
freq = 50
servo1 = GPIO.PWM(servo1_pin, freq)
servo2 = GPIO.PWM(servo2_pin, freq)

print ("Waiting for 2 seconds")
time.sleep(2)


print ("Rotation 180 degrees in 10 steps")

#Depend on the servo. Calibration is needed to be sure
MIN_DUTY = 2
MAX_DUTY = 10
CENTRE = MIN_DUTY + (MAX_DUTY - MIN_DUTY) / 2

# To avoid motor trembling
def no_stress():
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

servo1.start(MAX_DUTY)
servo2.start(MIN_DUTY)
time.sleep(1)
no_stress()

try:
    while True:
        time.sleep(4)    
        i = GPIO.input(PIR_SENSOR)
        k = 0 
        if i == 1:
            while k < 2:
                print ("Turning to 90 degrees")
                servo1.ChangeDutyCycle(MIN_DUTY)
                servo2.ChangeDutyCycle(MAX_DUTY)
                time.sleep(0.5)

                print("Turning back to 0 degrees")
                servo1.ChangeDutyCycle(MAX_DUTY)
                servo2.ChangeDutyCycle(MIN_DUTY)
                time.sleep(0.5)
                k = k + 1
                no_stress()
                time.sleep(1)
            
            #rubbing hands
            time.sleep(1)
            #pump running
            GPIO.output(relay_pin, GPIO.HIGH)
            time.sleep(5)
            #pump stopped
            GPIO.output(relay_pin, GPIO.LOW)
        elif i==0:
            no_stress()
            k = 0
            print("No motion")

except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    print("Cleaning up GPIO...")
    servo1.stop()
    servo2.stop()
    GPIO.output(relay_pin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.cleanup()


