#!/usr/bin/python

import time
from KK2 import KK2

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the BMP085 and use STANDARD mode (default value)
kk2 = KK2(0x08, debug=True)

#val = kk2.readTest()
#print "val: %04x" % val 

adj = 1234.56789

while True:
#  unscThrottle = kk2.readReg16b8(2)
#  rawRoll = kk2.readReg16b8(6)
#  rawPitch = kk2.readReg16b8(7)
#  rawThrottle = kk2.readReg16b8(8)
#  rawYaw = kk2.readReg16b8(9)
#  rawAux = kk2.readReg16b8(10)

#  roll,pitch,throttle,yaw,aux = kk2.readSticks(6,5)
  roll,pitch,throttle,yaw = kk2.readSticks(0,4)
  aux = kk2.readReg16b8(9)
  print "sticks: roll %d pitch %d throttle %d yaw %d aux %d" % (roll,pitch,throttle,yaw,aux)

#  print "raw roll %d pitch %d throttle %d yaw %d aux %d unsc. throttle %d" % (rawRoll,rawPitch,rawThrottle,rawYaw,rawAux,unscThrottle)

  kk2.writeReg16b8(12,adj) 
  adj += 0.1
  time.sleep(0.25)




