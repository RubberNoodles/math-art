from math import *
from Vector import *
from Surface import *

class Plane(Surface):
    def __init__(self, u0, u1, v0, v1, centre=[0.0, 0.0, 0.0],
                 uspan=[1.0, 0.0, 0.0], vspan=[0.0, 1.0, 0.0]):
        Surface.__init__(self, self.value, self.du, self.dv,
                         u0, u1, v0, v1, False, False)
        self.centre = centre
        self.uspan  = uspan
        self.vspan  = vspan
        
    def value(self, u, v):
        uweight = float(u - self.u0) / float(self.u1 - self.u0) - 0.5
        vweight = float(v - self.v0) / float(self.v1 - self.v0) - 0.5

        pu = ScalMult(uweight, self.uspan)
        pv = ScalMult(vweight, self.vspan)

        p = Add(pu, pv)

        return Add(self.centre, p)
    def du(self, u, v):
        uweight = 1.0 / float(self.u1 - self.u0)
        return ScalMult(uweight, self.uspan)
    def dv(self, u, v):
        vweight = 1.0 / float(self.v1 - self.v0)
        return ScalMult(vweight, self.vspan)
