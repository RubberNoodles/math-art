from math import sqrt, cos, sin, pi
from Vector import *

class Path:
    def __init__(self, value, deriv1, deriv2, deriv3, t0, t1,
                 cyclic=False):
        self.value = value
        self.deriv1 = deriv1
        self.deriv2 = deriv2
        self.deriv3 = deriv3
        self.t0 = t0
        self.t1 = t1
        self.cyclic = cyclic
