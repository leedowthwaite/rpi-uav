#!/usr/bin/python

import time
from srf02 import SRF02
from ema import EMA

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the sensor
srf02 = SRF02(0x70, debug=False)
# init EMA filter
rangeEMA = EMA(0.2)

while True:
  rangeCm = srf02.readRangeCentimeters()
  minRange = srf02.readMinRange()

  rangeFiltered = rangeEMA.filter(rangeCm)

#  rangeUs = srf02.readRangeMicroseconds()
#  print "range: %0.3f cm (min %0.3f; echo %0.3f ms)" % (rangeCm,minRange,rangeUs/1000.0)
  print "range: %0.2f cm filtered: %0.2f (min %0.3f)" % (rangeCm,rangeFiltered,minRange)
#  time.sleep(0.05)




