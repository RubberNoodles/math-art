from math import *
from Vector import *
from Surface import *
from Region import *

class SurfaceRegion(Surface):
    def __init__(self, surface, region):
        Surface.__init__(self, self.value, self.du, self.dv,
                         region.u0, region.u1, region.v0, region.v1,
                         uCyclic=region.uCyclic,
                         vCyclic=region.vCyclic)
        self.surface = surface
        self.region  = region

    def value(self, u, v):
        (ru, rv) = self.region.value(u,v)
        return (self.surface.value(ru, rv))
    def du(self, u, v):
        (ru,  rv)  = self.region.value(u,v)
        (dru, drv) = self.region.du(u,v)
        return (Add(ScalMult(dru, self.surface.du(ru, rv)), \
                ScalMult(rdv, self.surface.dv(ru, rv))))
    def dv(self, u, v):
        (ru,  rv)  = self.region.value(u,v)
        (rdu, rdv) = self.region.dv(u,v)
        return (Add(ScalMult(dru, self.surface.du(ru, rv)), \
                ScalMult(drv, self.surface.dv(ru, rv))))
