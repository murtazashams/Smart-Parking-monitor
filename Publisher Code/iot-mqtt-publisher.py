 #!/usr/bin/python3

#required libraries
import sys                                 
import ssl
import json
import paho.mqtt.client as mqtt

# for motion sensor
import RPi.GPIO as GPIO
import time
from datetime import datetime


#called while client tries to establish connection with the server 
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
        mqttc.subscribe("$aws/things/Raspberry-pi/shadow/update/acceptd", qos=0)
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="cgao")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/home/pi/aws_iot/rootCA.pem.crt",
	            certfile="/home/pi/aws_iot/f5337f8a50-certificate.pem.crt",
	            keyfile="/home/pi/aws_iot/f5337f8a50-private.pem.key",
              tls_version=ssl.PROTOCOL_TLSv1_2, 
              ciphers=None)

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("A178DX3B7UI70O.iot.us-west-2.amazonaws.com", port=8883) #AWS IoT service hostname and portno

#automatically handles reconnecting
#start a new thread handling communication with AWS IoT
mqttc.loop_start()

rc=0
try:
    while rc == 0:
 
       
      GPIO.setmode(GPIO.BCM)

 

      TRIG = 23

      ECHO = 24

      GPIO.setup(TRIG,GPIO.OUT)

      GPIO.setup(ECHO,GPIO.IN)
 

      GPIO.output(TRIG, False)

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
   
      playload = 'Distance: '+dist +' cm'
      print(playload)
    
      msg_info = mqttc.publish("$aws/things/Raspberry-pi/shadow/update", playload, qos=1)

      time.sleep(3)
      GPIO.cleanup()

except KeyboardInterrupt:
    pass

GPIO.cleanup()
