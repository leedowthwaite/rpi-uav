#!/usr/bin/python

import time
from srf02 import SRF02
from Adafruit_BMP085 import BMP085
from KK2 import KK2
from ema import EMA

# ===========================================================================
# Prototype system model
# ===========================================================================

class SystemModel:

  def __init__(self):
    # Initialise the sensors...
    # SFR02 ultrasonic rangefinder and filter
    self.srf02 = SRF02(0x70, debug=False)
    self.rangeEMA = EMA(0.2)
    # BMP085 barometer
    self.bmp085 = BMP085(0x77, BMP085.BMP085_HIGHRES,debug=False)  # HIRES Mode
    self.altitudeEMA = EMA(0.2)
    # the flight controller (modified KK2.0)
    self.kk2 = KK2(0x08, debug=False)
    self.calibrateGroundLevel()

  def calibrateGroundLevel(self):
    minRange = self.srf02.readMinRange()
    for i in range(32):
      self.readGroundRangefinder()
      self.readAltitude()
#    self.readGroundRangefinder()
    self.groundLevel = self.readAltitude()

  def readGroundRangefinder(self):
    rangeCm = self.srf02.readRangeCentimeters()
    rangeFiltered = self.rangeEMA.filter(rangeCm)
#    print "range: %0.2f cm filtered: %0.2f (min %0.3f)" % (rangeCm,rangeFiltered,minRange)
    return rangeFiltered


  def readAltitude(self):
    temp = self.bmp085.readTemperature()
    pressure = self.bmp085.readPressure()
    altitude = self.bmp085.readAltitude()
#    print "Temperature: %.2f C" % temp
#    print "Pressure:    %.2f hPa" % (pressure / 100.0)
#    print "Altitude:    %.2f" % altitude
    return self.altitudeEMA.filter(altitude)


  def isActive(self):
    return self.kk2.readUavMode()

  def update(self):
    groundRange = self.readGroundRangefinder()
    print "groundRange: ",groundRange

    altitude = self.readAltitude()
    print "altitude: ",altitude

    if (self.isActive()):
      try:
        roll,pitch,throttle,yaw = self.kk2.readSticks(0,4)
        print "sticks: roll %d pitch %d throttle %d yaw %d" % (roll,pitch,throttle,yaw)
      except IOError, e:
        print "Caught exception: ",e
#    kk2.writeReg16b8(12,adj)
 #   adj += 0.1
  #  time.sleep(0.25)
