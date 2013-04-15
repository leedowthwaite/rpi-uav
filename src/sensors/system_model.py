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
    self.desiredAltitude = 0
    self.rangeMin = self.srf02.readMinRange() / 100.0
    self.groundRangeValid = False
    print "min. range ",self.rangeMin

    self.throttleAdj = 0
#    print >>self.logFile, "calibrated ground level: %f" % self.groundLevel
    self.log("calibrated ground level: %f" % self.groundLevel)

  def log(self,line):
    print >>self.logFile, line

  def calibrateGroundLevel(self):
    minRange = self.srf02.readMinRange()
    for i in range(32):
#      self.readGroundRangefinder()
      self.groundLevel = self.readAbsAltitude()
      time.sleep(0.1)
#    self.readGroundRangefinder()
#    self.groundLevel = self.readAbsAltitude()

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
    if ((altitude > self.altitudeEMA.currentValue()+250) or (altitude < self.altitudeEMA.currentValue()-250)):
      print "WARNING: ignoring outlier altitude value: %0.2f" % altitude
      return self.altitudeEMA.currentValue()
    else:
      return self.altitudeEMA.filter(altitude)

  # returns filtered altitude relative to calibrated ground level
  def readAltitude(self):
    relAltitude = self.altitudeEMA.currentValue() - self.groundLevel
    return relAltitude

  # returns smart altitude based on combined barometer/rangefinder measurements
  def smartAltitude(self):
    relAltitude = self.altitudeEMA.currentValue() - self.groundLevel
    groundRange = self.rangeEMA.currentValue()
    if (self.groundRangeValid):
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
#    print "groundRange: %0.2f" % groundRange
    time.sleep(0.01)

    altitude = self.readAltitude()
#    print "rel. altitude: %0.2f" % altitude
    time.sleep(0.01)
    if (altitude > 0.5 and altitude < 3.0 and groundRange > self.rangeMin*2.0):
      self.groundRangeValid = True

    if (not self.groundRangeValid):
      groundRange = -1

    smartAltitude = self.smartAltitude()
#    print "smartAltitude: ",smartAltitude
    time.sleep(0.01)

    if (self.isActive()):

      # set desired altitude to current (alt. hold) if not already set
      if (self.desiredAltitude <= 0):
        self.desiredAltitude = smartAltitude
        print "alt hold mode: desiredAltitude set to %f" % (self.desiredAltitude)

      adjAltitude = self.desiredAltitude - smartAltitude
      if (abs(adjAltitude) > 0.01):
#        if (abs(self.throttleAdj) < 500):
        self.throttleAdj = self.throttleAdj + adjAltitude*10.0

      roll = pitch = throttle = yaw = 0
      try:
        roll,pitch,throttle,yaw = self.kk2.readSticks(0,4)
#        print "sticks: roll %d pitch %d throttle %d yaw %d" % (roll,pitch,throttle,yaw)
      except IOError, e:
        print "Caught exception: ",e
      time.sleep(0.01)

      self.kk2.writeReg16b8(KK2.KK2_UAV_THROTTLE_ADJ,self.throttleAdj)
      self.log("groundRange %f rel.alt %f smartAltitude %f adjAltitude %f throttleAdj %f" % (groundRange, altitude, smartAltitude, adjAltitude, self.throttleAdj))
      print "smartAltitude %0.2f groundRange %0.2f adjAltitude %0.2f throttle %d throttleAdj %0.2f" % (smartAltitude, groundRange, adjAltitude, throttle, self.throttleAdj)

    else:
      self.throttleAdj = 0
      self.groundRangeValid = False

