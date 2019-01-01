#IMPORT ALL NECESSARY MODULES
import requests
import RPi.GPIO as GPIO
import time
from gpiozero import MotionSensor

#CONFIGURE GPIO PINS
GPIO.setmode(GPIO.BCM) #set the GPIO naming convention to broadcom (pin numbering)
GPIO.setwarnings(False) #disable GPIO warnings (GPIO.cleanup() sets any GPIO you have used within RPi.GPIO to INPUT mode)
GPIO.setup(18,GPIO.OUT) #define GPIO 18 as OUT for when motion signal is sent
pir = MotionSensor(14) #define GPIO 14 as input pin for MotionSensor

motionTrigger = 0 #motionTrigger is the variable that will be toggled when the PiR sensor detects motion

while True: #set up a never ending loop

    #everytime the loop starts, turn off both motion LED pins
    GPIO.output(18,GPIO.LOW)  

    if motionTrigger == 1: #if motion was detected in the last cycle:

        print('sending active signal...')

        GPIO.output(18,GPIO.HIGH) #turn on the motion signal LED

        #configure the web server request
        params = (
            ('nid','2'), #node id
            ('signal', 'active'), #status
        )
        response = requests.get('http://evansteiner.com/ralipoint/update.php', params=params) #send request

    else: #if no motion was detected

        print ('sending inactive signal...')

        #configure the web server request
        params = (
            ('nid','2'), #node id
            ('signal', 'inactive'), #status
        )
        response = requests.get('http://evansteiner.com/ralipoint/update.php', params=params) #send request

    count = 0 #set/reset the motion loop counter to 0
    motionTrigger = 0 #resent the motionTrigger to 0

    while (count < 10): #each loop sleeps for one second, so this cycle should take ~10 seconds
        if pir.motion_detected:

            print('motion detected...')

            motionTrigger = 1 #set the flag so that the detected motion signal will be sent to the server
            
        count = count + 1 #increment the count
        time.sleep(1) #sleep for one second
