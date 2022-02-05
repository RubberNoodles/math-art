from math import *
from Vector import *
from Surface import *

class MorphSurface(Surface):
    def __init__(self, surface1, surface2):
        uCyclic = surface1.uCyclic and surface2.uCyclic
        vCyclic = surface1.vCyclic and surface2.vCyclic
        u0 = max(surface1.u0, surface2.u0)
        u1 = min(surface1.u1, surface2.u1)
        v0 = max(surface1.v0, surface2.v0)
        v1 = min(surface1.v1, surface2.v1)
        Surface.__init__(self, self.value, self.du, self.dv,
                         u0, u1, v0, v1, uCyclic, vCyclic)
        self.surface1 = surface1
        self.surface2 = surface2
        self.weight = 0.0
    def setweight(self, weight):
        self.weight = weight
        
    def value(self, u, v):
        a = ScalMult(1.0 - self.weight, self.surface1.value(u, v))
        b = ScalMult(self.weight,     self.surface2.value(u, v))
        return (Add(a, b))
    def du(self, u, v):
        a = ScalMult(1.0 - self.weight, self.surface1.du(u, v))
        b = ScalMult(self.weight,     self.surface2.du(u, v))
        return (Add(a, b))
    def dv(self, u, v):
        a = ScalMult(1.0 - self.weight, self.surface1.dv(u, v))
        b = ScalMult(self.weight,     self.surface2.dv(u, v))
        return (Add(a, b))
