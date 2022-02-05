from math import *
from Vector import *
from Region import *

class CircleRegion(Region):
    def __init__(self, center, radius, phase=0):
        Region.__init__(self, self.value, self.du, self.dv,
                        0.0, 1.0, 0.0, 1.0,
                        uCyclic=True, vCyclic=False)
        self.center   = center
        self.radius   = radius
        self.phase    = phase

    def get_theta(self, u):
        return (self.phase + 2*pi*u)

    def value(self, u, v):
        theta = self.get_theta(u)
        ru = self.center[0] + v * self.radius * cos(theta)
        rv = self.center[1] + v * self.radius * sin(theta)
        return (ru, rv)
    def du(self, u, v):
        theta = self.get_theta(u)
        ru = -v * self.radius * sin(theta) * 2 * pi
        rv =  v * self.radius * cos(theta) * 2 * pi
        return (ru, rv)
    def dv(self, u, v):
        theta = self.get_theta(u)
        ru = self.radius * cos(theta)
        rv = self.radius * sin(theta)
        return (ru, rv)
