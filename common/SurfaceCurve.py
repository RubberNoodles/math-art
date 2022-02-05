from math import sqrt, cos, sin, pi
from Vector import *
from Curve import *

class SurfaceCurve(Curve):
    def __init__(self, surface, path):
        self.surface = surface
        self.path    = path
        """
        Curve.__init__(self, self.value, self.deriv1, self.deriv2,
                       self, deriv3. path.t0, path.t1, unitSpeed=False,
                       cyclic=path.cyclic)
        """
        self.t0 = path.t0
        self.t1 = path.t1
        self.unitSpeed=False
        self.cyclic = path.cyclic

    def value(self, t):
        (u, v) = self.path.value(t)
        return self.surface.value(u,v)

    def tangent(self,t):
        (u, v) = self.path.value(t)
        (dpu, dpv) = self.path.deriv1(t)
        dsu = self.surface.du(u, v)
        dsv = self.surface.dv(u, v)

        a = ScalMult(dpu, dsu)
        b = ScalMult(dpv, dsv)
        return Normalize(Add(a,b))

    def normal(self, t):
        (u, v) = self.path.value(t)
        return self.surface.normal(u, v)

    def binormal(self, t):
        return Cross(self.tangent(t), self.normal(t))
  
    """
    def deriv1(self, t):
        (u, v) = self.path.value(t)
        (dpu, dpv) = self.path.deriv1(t)
        dsu = self.surface.du(u, v)
        dsv = self.surface.dv(u, v)

        a = ScalMult(dpu, dsu)
        b = ScalMult(dpv, dsv)
        return Add(a,b)

    def deriv2(self, t):
        (u, v) = self.path.value(t)
        (dpu, dpv) = self.path.deriv1(t)
        (dpu2, dpv2) = self.path.deriv2(t)
        
    """
