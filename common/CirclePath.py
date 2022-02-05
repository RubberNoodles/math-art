from math import *
from Vector import *
from Path import *

class CirclePath(Path):
    def __init__(self, center, radius, phase=0, angle=2*pi, cyclic=True):
        Path.__init__(self, self.value, self.deriv1,
                      self.deriv2, self.deriv3, 0.0, 1.0,
                      cyclic=cyclic)
        self.center   = center
        self.radius   = radius
        self.phase    = phase
        self.angle    = angle
        self.dtheta   = self.angle / (self.t1 - self.t0)
        self.rdtheta  = self.radius * self.dtheta
        self.rdtheta2 = self.rdtheta * self.dtheta
        self.rdtheta3 = self.rdtheta2 * self.dtheta

    def get_theta(self, t):
        return (self.phase + self.dtheta * (t - self.t0))
    def value(self, t):
        theta = self.get_theta(t)
        x = self.center[0] + self.radius * cos(theta)
        y = self.center[1] + self.radius * sin(theta)
        return (x,y)
    def deriv1(self, t):
        theta = self.get_theta(t)
        x = -self.rdtheta * sin(theta)
        y =  self.rdtheta * cos(theta)
        return (x,y)
    def deriv2(self, t):
        theta = self.get_theta(t)
        x = -self.rdtheta2 * cos(theta)
        y = -self.rdtheta2 * sin(theta)
        return (x,y)
    def deriv3(self, t):
        theta = self.get_theta(t)
        x =  self.rdtheta3 * sin(theta)
        y = -self.rdtheta3 * cos(theta)
        return (x,y)
