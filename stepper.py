#!/usr/bin/python37all
import RPi.GPIO as GPIO
import time
from PCF8591 import PCF8591
GPIO.setmode(GPIO.BCM)
ledPin = 26
GPIO.setup(ledPin, GPIO.OUT)

pins = [18,21,22,23] # controller inputs: in1, in2, in3, in4
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

sequence = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
             [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
state = 0

def halfstep(dir):
  global state
  # dir = +/- 1 (ccw / cw)
  state += dir
  if state > 7: state = 0
  elif state < 0: state =  7
  for pin in range(4):    # 4 pins that need to be energized
    GPIO.output(pins[pin], sequence[state][pin])
  delay_us(1000)

def moveSteps(steps, dir):
  # move the actuation sequence a given number of half steps
  for x in range(int(steps)):
    halfstep(dir)

def delay_us(tus): # use microseconds to improve time resolution
  endTime = time.time() + float(tus)/ float(1E6)
  while time.time() < endTime:
    pass

class Stepper:
  currentAngle = 0;
  def __init__(self, address):
    self.address = PCF8591(address)
  def goAngle(self,angle):
    
    if abs(int(angle) - Stepper.currentAngle) < 180 and int(angle) > Stepper.currentAngle:
      newAngle = abs(Stepper.currentAngle - int(angle))
      steps = int(newAngle)*(4096/360)
      moveSteps(steps, 1)
      Stepper.currentAngle = angle
    elif abs(angle - Stepper.currentAngle) < 180 and int(angle) <= Stepper.currentAngle:
      newAngle = abs(int(angle) - Stepper.currentAngle)
      steps = int(newAngle)*(4096/360)
      moveSteps(steps, -1)
      Stepper.currentAngle = angle
    elif abs(int(angle) - Stepper.currentAngle)>=180 and int(angle) > Stepper.currentAngle:
      newAngle = abs(int(angle)-Stepper.currentAngle - 360)
      steps = int(newAngle)*(4096/360)
      moveSteps(steps, 1)
      Stepper.currentAngle = angle
    else:
      newAngle = abs(abs(angle-Stepper.currentAngle)-360)
      steps = int(newAngle)*(4096/360)
      moveSteps(steps, -1)
      Stepper.currentAngle = angle
      
  def zero(self):
    GPIO.output(ledPin,1)
    while int(self.address.read(0)) <= 200: 
      moveSteps(1,1) 
      time.sleep(.01)
    GPIO.output(ledPin,0)
    Stepper.currentAngle = 0

step = Stepper(40)
step.goAngle(30)


