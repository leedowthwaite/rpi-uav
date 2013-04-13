#!/usr/bin/python

import time

class EMA:

  def __init__(self, coeff):
    self.coeff = coeff
    self.x0 = 0
    self.y = 0

  def filter(self, x):
    # y = coeff * x + (1.0f-coeff) * x0
    self.y = self.coeff * x + (1.0-self.coeff) * self.x0
    self.x0 = self.y
    return self.y

  def currentValue(self):
    return self.y
