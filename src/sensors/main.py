#!/usr/bin/python

import time
from system_model import SystemModel
from threading import Timer
import RPi.GPIO as GPIO

systemModel = None
timer = None

def serviceTimer():
#  print "--- serviceTimer() ---"
  systemModel.update()
  timer = Timer(0.1, serviceTimer)
  timer.start()

# ===========================================================================
# Prototype system model
# ===========================================================================

GPIO.setmode(GPIO.BCM)
GPIO.setup(8,GPIO.OUT)
# reset KK2
GPIO.output(8,GPIO.LOW)
time.sleep(0.05)
GPIO.output(8,GPIO.HIGH)
time.sleep(4)

print "initializing system model"
systemModel = SystemModel()
print "system model initialized, ground level calibrated to ",systemModel.groundLevel
desiredAltitude = 2
#print "setting desired (rel.) altitude to ",desiredAltitude
#systemModel.setDesiredAltitude( desiredAltitude )

timer = Timer(0.1, serviceTimer)
timer.start()

while True:
  print "idle"
  time.sleep(1)

GPIO.cleanup()


