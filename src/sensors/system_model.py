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
    # open log file
    self.logFile = open('system_model_log.txt', 'w')

    # Initialise the sensors...
    # SFR02 ultrasonic rangefinder and filter
    self.srf02 = SRF02(0x70, debug=False)
    self.rangeEMA = EMA(0.2)
    # BMP085 barometer
    self.bmp085 = BMP085(0x77, BMP085.BMP085_HIGHRES,debug=False)  # HIRES Mode
    self.altitudeEMA = EMA(0.2)
    # the flight controller (modified KK2.0)
    self.kk2 = KK2(0x08, debug=False)
    self.groundLevel = 0
    self.calibrateGroundLevel()
    self.desiredAltitude = self.groundLevel
    self.rangeMin = self.srf02.readMinRange() / 100.0
    print "min. range ",self.rangeMin

    self.throttleAdj = 0
#    print >>self.logFile, "calibrated ground level: %f" % self.groundLevel
    self.log("calibrated ground level: %f" % self.groundLevel)

  def log(self,line):
    print >>self.logFile, line

  def calibrateGroundLevel(self):
    minRange = self.srf02.readMinRange()
    for i in range(32):
      self.readGroundRangefinder()
      self.readAbsAltitude()
#    self.readGroundRangefinder()
    self.groundLevel = self.readAbsAltitude()

  def readGroundRangefinder(self):
    range = self.srf02.readRangeCentimeters() / 100.0
    rangeFiltered = self.rangeEMA.filter(range)
    return rangeFiltered

  def readAbsAltitude(self):
    temp = self.bmp085.readTemperature()
    pressure = self.bmp085.readPressure()
    altitude = self.bmp085.readAltitude()
#    print "Temperature: %.2f C" % temp
#    print "Pressure:    %.2f hPa" % (pressure / 100.0)
#    print "Altitude:    %.2f" % altitude
    return self.altitudeEMA.filter(altitude)

  # returns filtered altitude relative to calibrated ground level
  def readAltitude(self):
    relAltitude = self.altitudeEMA.currentValue() - self.groundLevel
    return relAltitude

  # returns smart altitude based on combined barometer/rangefinder measurements
  def smartAltitude(self):
    relAltitude = self.altitudeEMA.currentValue() - self.groundLevel
    groundRange = self.rangeEMA.currentValue()
    if (relAltitude > 0.25 and groundRange > self.rangeMin*2.0):
      return (relAltitude + groundRange) / 2.0
    else:
      return relAltitude


  def setDesiredAltitude(self, desiredAltitude):
    self.desiredAltitude = desiredAltitude
    self.log("desiredAltitude set to %f" % self.desiredAltitude)

  def isActive(self):
    return self.kk2.readUavMode()

  def update(self):
    # update measurements
    self.readGroundRangefinder()
    self.readAbsAltitude()

    groundRange = self.rangeEMA.currentValue()
    print "groundRange: ", groundRange

    altitude = self.readAltitude()
    print "rel. altitude: ",altitude

    smartAltitude = self.smartAltitude()
    print "smartAltitude: ",smartAltitude

    if (self.isActive()):

      adjAltitude = self.desiredAltitude - altitude
      print "adjAltitude: ",adjAltitude
      if (adjAltitude > 0.05):
        if (self.throttleAdj < 200):
          self.throttleAdj = self.throttleAdj + 1
      elif (adjAltitude < -0.05):
        if (self.throttleAdj > -200):
          self.throttleAdj = self.throttleAdj - 1
      print "throttleAdj ",self.throttleAdj

      try:
        roll,pitch,throttle,yaw = self.kk2.readSticks(0,4)
        print "sticks: roll %d pitch %d throttle %d yaw %d" % (roll,pitch,throttle,yaw)
      except IOError, e:
        print "Caught exception: ",e

      self.kk2.writeReg16b8(KK2.KK2_UAV_THROTTLE_ADJ,self.throttleAdj)
      self.log("groundRange %f rel.alt %f smartAltitude %f adjAltitude %f throttleAdj %f" % (groundRange, altitude, smartAltitude, adjAltitude, self.throttleAdj))


