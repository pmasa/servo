import RPi.GPIO as GPIO
import time

import threading 


GPIO.setmode(GPIO.BCM)

relay_pin = 27
servo1_pin = 6
servo2_pin = 5
PIR_SENSOR = 17

GPIO.setup(PIR_SENSOR, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
GPIO.setup(relay_pin, GPIO.OUT)

# Create PWM channel on the servo pin with a frequency of 50Hz
freq = 50
servo1 = GPIO.PWM(servo1_pin, freq)
servo2 = GPIO.PWM(servo2_pin, freq)

print ("Waiting for 2 seconds")
time.sleep(2)


print ("Start processing...")

#Depend on the servo. Calibration is needed to be sure
MIN_DUTY = 2
MAX_DUTY = 10
CENTRE = MIN_DUTY + (MAX_DUTY - MIN_DUTY) / 2

stop = False
motion = False

i = GPIO.input(PIR_SENSOR)
time.sleep(5) # wait 5 seconds for PIR to reset.

class Monthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.encore = True # variable pour arreter le thread sur demande
        self.enpause = False # variable pour mettre le thread en pause

        self.c = 0 # simple compteur pour affichage
	self.previous_state = 0
	self.current_state = 0

    def run(self):
        global motion
        while self.encore:

            while self.enpause:
                time.sleep(15)

            # activite du thread
            # ...
	    self.current_state  = GPIO.input(PIR_SENSOR)
	    time.sleep(4) # wait 4 seconds for PIR to reset.
	    if self.previous_state == 0  and self.current_state == 1:
		motion = True
	    else:
		print("no motion")
	    self.previous_state  = self.current_state
            #self.c += 1
            #print self.c
            # ...

    def pause(self):
        self.enpause = True
	print("thread en pause...")

    def reprise(self):
        self.enpause = False
	print("reprise thread...")

    def stop(self):
        self.encore = False


# To avoid motor trembling
def no_stress():
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

servo1.start(MAX_DUTY)
servo2.start(MIN_DUTY)
time.sleep(1)
no_stress()

app=Monthread()
app.start()

try:
    while True:
        time.sleep(1)    
        #i = GPIO.input(PIR_SENSOR)
        k = 0 
        #if i == 1 and busy == False:
	if app.isAlive() and motion:
	    app.pause()
            while k < 1:
                print ("Turning to 90 degrees")
                servo1.ChangeDutyCycle(MIN_DUTY)
                servo2.ChangeDutyCycle(MAX_DUTY)
                time.sleep(0.5)

                print("Back to initial degrees")
                servo1.ChangeDutyCycle(MAX_DUTY)
                servo2.ChangeDutyCycle(MIN_DUTY)
                time.sleep(0.5)
                k = k + 1
                no_stress()
                time.sleep(1)
            
	    print("Rubbing hands ...")
            time.sleep(5)

	    print("Open pump")
            GPIO.output(relay_pin, GPIO.HIGH)
            time.sleep(5)

	    print("Pump stopped")
            GPIO.output(relay_pin, GPIO.LOW)
	    motion = False
	    time.sleep(5)
	    app.reprise()
	#if z > 20:
	#    z = 0
        #elif i==0:
	#    busy = False
        #    no_stress()
        #    k = 0
        #    print("No motion")

except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    print("Cleaning up GPIO...")
    app.stop() 
    servo1.stop()
    servo2.stop()
    GPIO.output(relay_pin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.cleanup()


