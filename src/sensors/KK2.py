#!/usr/bin/python

import time
import math
from Adafruit_I2C import Adafruit_I2C

# ===========================================================================
# KK2 Class
# ===========================================================================

class KK2 :
  i2c = None

  KK2_UAV_ROLL_ADJ      = 10
  KK2_UAV_PITCH_ADJ     = 11
  KK2_UAV_THROTTLE_ADJ  = 12

  # KK2 Registers
  __KK2_CMD           = 0x00  
  __KK2_TEST          = 0x06

  # Constructor
  def __init__(self, address=0x08, debug=False):
    self.i2c = Adafruit_I2C(address,debug=debug,byteSwap=False)

    self.address = address
    self.debug = debug

  def readTest(self):
#    self.i2c.write8(self.__KK2_CMD, 0x55)
#    time.sleep(0.005)  # Wait 5ms
    raw = self.i2c.readU8(0x0f)
    if (self.debug):
      print "DBG: raw result: 0x%04X (%d)" % (raw & 0xFFFF, raw)
    return raw

  def readStatus(self):
    val = self.i2c.readU8(0xff)
    return val

  def readUavMode(self):
    status = self.readStatus()
    return (status != 0)

  def readReg16(self, reg):
    val = self.i2c.readS16(reg)
    return val

  def listTo16b8(self,valh,vall,valf):
    val = float(valh)*256.0 + float(vall) + (float(valf)/256.0)
    if val >= 32768:
      val = val-65536
    return val

  def readReg16b8(self, reg):
    list = self.i2c.readList(reg,3)
    print "list: ",list
    val = self.listTo16b8(list[0],list[1],list[2])
    return val

  def writeReg16b8(self, reg, data):
    df,di = math.modf(data)
    list = [int(int(di)/256), int(int(data)&0xff), int(df*256.0)]
    self.i2c.writeList(reg,list)



  def readSticks(self,base,nsticks):
    lst = self.i2c.readList(base,nsticks*3)
#    print "list: ",lst
    if (isinstance(lst, list)):
      res = []
      for i in range(nsticks):
        res.append (self.listTo16b8(lst[i*3],lst[i*3+1],lst[i*3+2]))
      return res
    else:
      raise (IOError, "Error reading sticks")


