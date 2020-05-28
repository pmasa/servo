import RPi.GPIO as GPIO
import time

import threading 


GPIO.setmode(GPIO.BCM)

relay_pin = 27
PIR_SENSOR = 17

GPIO.setup(PIR_SENSOR, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(relay_pin, GPIO.OUT)


print ("Waiting for 2 seconds")
time.sleep(2)


print ("Start processing...")

motion = False

i = GPIO.input(PIR_SENSOR)
time.sleep(5) # wait 5 seconds for PIR to reset.

class Monthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.encore = True # variable pour arreter le thread sur demande
        self.enpause = False # variable pour mettre le thread en pause

	self.previous_state = 1
	self.current_state = 0

    def run(self):
        global motion
        while self.encore:

            while self.enpause:
                time.sleep(1)

	    self.current_state  = GPIO.input(PIR_SENSOR)
	    #if self.previous_state == 0  and self.current_state == 1:
	    if self.current_state == 1:
		motion = True
		self.previous_state  = 1
		print("motion")
	    else:
		motion = False
		print("no motion")
		self.previous_state = 0
	    time.sleep(3)		

    def pause(self):
        self.enpause = True
	print("thread en pause...")

    def reprise(self):
        self.enpause = False
	print("reprise thread...")

    def stop(self):
        self.encore = False


mon_thread = Monthread()
mon_thread.start()

try:
    while True:
        time.sleep(0.5)    
	if mon_thread.isAlive() and motion:
	    mon_thread.pause()
            
	    print("Open pump")
            GPIO.output(relay_pin, GPIO.HIGH)
            time.sleep(0.005)

	    print("Pump stopped")
            GPIO.output(relay_pin, GPIO.LOW)
	    motion = False
	    time.sleep(10)
	    mon_thread.reprise()

except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    print("Cleaning up GPIO...")
    mon_thread.stop() 
    GPIO.output(relay_pin, GPIO.LOW)
    GPIO.cleanup()


