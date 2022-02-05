from math import *
from Vector import *
from Surface import *

class OffsetSurface(Surface):
    def __init__(self, surface, offset):
        Surface.__init__(self, self.value, self.du, self.dv,
                         surface.u0, surface.u1,
                         surface.v0, surface.v1,
                         uCyclic=surface.uCyclic,
                         vCyclic=surface.vCyclic)
        self.surface  = surface
        self.offset   = offset
    def value(self, u, v):
        X = self.surface.value(u,v)
        n = self.surface.normal(u,v)
        return (Add(X, ScalMult(self.offset, n)))
    def du(self, u, v):
        return (self.surface.du(u, v))
    def dv(self, u, v):
        return (self.surface.dv(u, v))
