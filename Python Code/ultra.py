import RPi.GPIO as GPIO

import time

x = 1
while x == 1:
      GPIO.setmode(GPIO.BCM)

 

      TRIG = 23

      ECHO = 24



    

      #print "Distance Measurement In Progress"

 

      GPIO.setup(TRIG,GPIO.OUT)

      GPIO.setup(ECHO,GPIO.IN)

 

      GPIO.output(TRIG, False)

      #print "Waiting For Sensor To Settle"

      time.sleep(2)

 

      GPIO.output(TRIG, True)

      time.sleep(0.00001)

      GPIO.output(TRIG, False)

 

      while GPIO.input(ECHO)==0:

          pulse_start = time.time()

 

      while GPIO.input(ECHO)==1:

          pulse_end = time.time()

 

      pulse_duration = pulse_end - pulse_start

 

      distance = pulse_duration * 17150

 

      distance = round(distance, 2)
      dist = str(distance)
      
      
      
      print "Distance:",distance,"cm"
      f = open("/var/www/html/out.txt", "wb")
      f.write(dist)
      f.close()

      time.sleep(3)

    
      GPIO.cleanup()
