#!/usr/bin/python

import time
from srf02 import SRF02

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the BMP085 and use STANDARD mode (default value)
srf02 = SRF02(0x70, debug=False)

while True:
  range = srf02.readRangeCentimeters()
  print "range(cm): %d" % (range)
#  range = srf02.readRangeMicroseconds()
 # print "range(us): %d" % (range)
  time.sleep(0.1)




