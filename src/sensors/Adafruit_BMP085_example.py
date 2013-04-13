#!/usr/bin/python

from Adafruit_BMP085 import BMP085

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the BMP085 and use STANDARD mode (default value)
#bmp = BMP085(0x77, debug=True)
#bmp = BMP085(0x77)

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, BMP085.BMP085_ULTRALOWPOWER)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, BMP085.BMP085_STANDARD)  # STANDARD Mode
 bmp = BMP085(0x77, BMP085.BMP085_HIGHRES)  # HIRES Mode
# bmp = BMP085(0x77, BMP085.BMP085_ULTRAHIGHRES)  # ULTRAHIRES Mode

temp = bmp.readTemperature()
pressure = bmp.readPressure()
altitude = bmp.readAltitude()

print "Temperature: %.2f C" % temp
print "Pressure:    %.2f hPa" % (pressure / 100.0)
print "Altitude:    %.2f" % altitude
