#!/usr/bin/python

import time
from system_model import SystemModel
from threading import Timer

systemModel = None
timer = None

def serviceTimer():
  print "--- serviceTimer() ---"
  systemModel.update()
  timer = Timer(0.1, serviceTimer)
  timer.start()

# ===========================================================================
# Prototype system model
# ===========================================================================

systemModel = SystemModel()
timer = Timer(0.1, serviceTimer)
timer.start()

while True:
  print "idle"
  time.sleep(1)




