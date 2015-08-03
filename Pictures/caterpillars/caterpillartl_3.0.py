import shutil
import time
import picamera
import datetime as dt
import RPi.GPIO as GPIO

#Set up the Pins. 23 & 24 each switch 3 IR LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


with picamera.PiCamera() as camera:
	camera.led = False
	camera.resolution = (640,480)
	camera.rotation = 270
	for filename in camera.capture_continuous('01caterpillar{counter:04d}.jpg'):
		#turn IR lights off
		GPIO.output(23,0)
		GPIO.output(24,0)

		print ('Captured %s' % filename)

		#copy latest picture to www for webcam
		shutil.copy(filename, "/var/www/images/caterpillars.jpg")
		print ('copied file to webcam')
		time.sleep(58)

                #add a timestamp to the picture 
                timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.annotate_text=(timestamp)

		#is it time to turn on the IR lights?
		start = dt.time(4, 30) 
		end = dt.time(11)
		currentTime = dt.datetime.now().time()
		if (start <= currentTime <= end):
			time.sleep(2) 
		else: 
			#turn IR lights on for next picture
	                GPIO.output(23, 1)
        	        GPIO.output(24, 1)
                	time.sleep(2)
