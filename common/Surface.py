from Vector import *

class Surface:
    def __init__(self, value, du, dv, u0, u1, v0, v1,
                 uCyclic=False, vCyclic=False,
                 red=None, red0=None, red1=None,
                 green=None, green0=None, green1=None,
                 blue=None, blue0=None, blue1=None):
        self.value = value
        self.du = du
        self.dv = dv
        self.u0 = u0
        self.u1 = u1
        self.v0 = v0
        self.v1 = v1
        self.uCyclic = uCyclic
        self.vCyclic = vCyclic
        self.red = red
        self.red0 = red0
        self.red1 = red1
        self.green = green
        self.green0 = green0
        self.green1 = green1
        self.blue = blue
        self.blue0 = blue0
        self.blue1 = blue1
    def normal(self, u, v):
        return Normalize(Cross(self.du(u, v), self.dv(u, v)))
