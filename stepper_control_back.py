#!/usr/bin/python37all
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from stepper import Stepper
import json
from urllib.request import urlopen # use to send/receive data
from urllib.parse import urlencode # use to structure a GET string
import time
api = "Y0O61FF5ZVI5VQ7W" # Enter your API key
while True:
  with open('stepper.txt', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

  step = Stepper(0x48)
  if data["button"] == "Zero":
    step.zero() 

  
  if data["button"] == "Change Angle":
    step.goAngle(int(data["slider1"]))
  
  
  
  params = {
    1: data["slider1"],
    "api_key":api}
  
  params = urlencode(params) # reformat dictionary as a GET string
  url = "https://api.thingspeak.com/update?" + params
  response = urlopen(url) # open the URL
  print(response.status, response.reason) # display request response
  time.sleep(16) # 15 sec minimum




