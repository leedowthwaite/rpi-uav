#!/usr/bin/python

import time
from Adafruit_I2C import Adafruit_I2C

# ===========================================================================
# SRF02 Class
# ===========================================================================

class SRF02 :
  i2c = None

  # Default I2C address
  __I2CADDR                 = 0x70

  # SRF02 Registers
  # read mode
  __SRF02_R_SWREVISION      = 0x00
  __SRF02_R_UNUSED          = 0x01
  __SRF02_R_RANGEH          = 0x02
  __SRF02_R_RANGEL          = 0x03
  __SRF02_R_AUTOTUNEMINH    = 0x04
  __SRF02_R_AUTOTUNEMINL    = 0x05
  # write mode
  __SRF02_COMMAND           = 0x00

  # commands
  __SRF02_CMD_RRM_INCHES        = 0x50
  __SRF02_CMD_RRM_CENTIMETERS   = 0x51
  __SRF02_CMD_RRM_MICROSECONDS  = 0x52
  __SRF02_CMD_FRM_INCHES        = 0x56
  __SRF02_CMD_FRM_CENTIMETERS   = 0x57
  __SRF02_CMD_FRM_MICROSECONDS  = 0x58
  __SRF02_CMD_8x40KHZ_BURST     = 0x5c
  __SRF02_CMD_AUTOTUNE_RESTART  = 0x60
  __SRF02_CMD_CHANGE_ADDR_SEQ1  = 0xa0
  __SRF02_CMD_CHANGE_ADDR_SEQ2  = 0xa5
  __SRF02_CMD_CHANGE_ADDR_SEQ3  = 0xaa

  # Constructor
  def __init__(self, address=__I2CADDR, debug=False):
    self.i2c = Adafruit_I2C(address,debug=debug,byteSwap=True)
    self.address = address
    self.debug = debug

  def readRange(self, rangingMode):
    "Reads the range reported by the sensor (in inches)"
    self.i2c.write8(self.__SRF02_COMMAND, rangingMode)
    time.sleep(0.070)  # Wait more than 65ms
    range = self.i2c.readU16(self.__SRF02_R_RANGEH)
    if (self.debug):
      print "DBG: Range(in): %d" % (range)
    return range

  def readRangeInches(self):
    "Reads the range reported by the sensor (in inches)"
    return self.readRange(self.__SRF02_CMD_RRM_INCHES)

  def readRangeCentimeters(self):
      "Reads the range reported by the sensor (in cm)"
      return self.readRange(self.__SRF02_CMD_RRM_CENTIMETERS)

  def readRangeMicroseconds(self):
      "Reads the range reported by the sensor (in us)"
      return self.readRange(self.__SRF02_CMD_RRM_MICROSECONDS)


