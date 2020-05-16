import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

servo_pin = 6
servo2_pin = 5

GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Create PWM channel on the servo pin with a frequency of 50Hz
freq = 50
servo = GPIO.PWM(servo_pin, freq)
servo2 = GPIO.PWM(servo2_pin,freq)

print ("Waiting for 2 seconds")
time.sleep(2)


print ("Rotation 180 degrees in 10 steps")

PIR_SENSOR = 23
GPIO.setup(PIR_SENSOR, GPIO.IN)

#Depend on the servo. Calibration is needed to be sure
MIN_DUTY = 2
MAX_DUTY = 10
CENTRE = MIN_DUTY + (MAX_DUTY - MIN_DUTY) / 2

# To avoid motor trembling
def no_stress():
    servo.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

servo.start(MAX_DUTY)
servo2.start(MIN_DUTY)
time.sleep(1)
no_stress()

while True:
    time.sleep(4)    
    i = GPIO.input(PIR_SENSOR)
    k = 0 
    if i == 1:
        while k < 2:
            print ("Turning to 90 degrees")
	    servo.ChangeDutyCycle(MIN_DUTY)
            servo2.ChangeDutyCycle(MAX_DUTY)
            #servo2.ChangeDutyCycle(12.5)
            time.sleep(0.5)

            print("Turning back to 0 degrees")
            servo.ChangeDutyCycle(MAX_DUTY)
            servo2.ChangeDutyCycle(MIN_DUTY)
            time.sleep(0.5)
            k = k + 1
	    no_stress()
            time.sleep(1)
    elif i==0:
	no_stress()
        k = 0
        print("No motion")
            
servo.stop()
servo2.stop()
GPIO.cleanup()


