from math import sqrt, cos, sin, pi
from Vector import *

class Curve:
    def __init__(self, value, deriv1, deriv2, deriv3, t0, t1,
                 unitSpeed=False, arcResolution = 1000,
                 cyclic=False, planar=False, linear = False):
    #constructor
        self.value = value
        self.deriv1 = deriv1
        self.deriv2 = deriv2
        self.deriv3 = deriv3
        self.t0 = t0
        self.t1 = t1
        self.cyclic = cyclic
        self.planar = planar
        
        

        if (unitSpeed ==True): #Unit speed amount
            self.tangent   = self.tangentUnitSpeed
            self.normal    = self.normalUnitSpeed
            self.binormal  = self.binormalUnitSpeed
            self.curvature = self.curvatureUnitSpeed
            self.torsion   = self.torsionUnitSpeed
            self.arclength = self.arcLengthUnitSpeed

            
        else: #Regular speed
            self.tangent   = self.tangentArbitrarySpeed
            self.normal    = self.normalArbitrarySpeed
            self.binormal  = self.binormalArbitrarySpeed
            self.curvature = self.curvatureArbitrarySpeed
            self.torsion   = self.torsionArbitrarySpeed
            self.arclength = self.arcLengthArbitrarySpeed
            self.arcResolution = arcResolution
        
        if linear: #linear case, use oriented normal
            self.normal = self.orientedNormal
            self.binormal = self.binormalArbitrarySpeed
            #self.torsion = self.torsion2d
            
        if (planar==True): #Planar case
            self.normal = self.orientedNormal
            self.binormal = self.binormal2d
            self.torsion = self.torsion2d
            if (unitSpeed ==True):
                self.curvature = self.oCurvatureUnitSpeed
            else:
                self.curvature = self.oCurvatureArbitrarySpeed
    #Arbitrary speed 
    def tangentArbitrarySpeed(self, t):
        return self.deriv1(t)
    
    def normalArbitrarySpeed(self,t):
        return Normalize(self.deriv2(t))
    
    def binormalArbitrarySpeed(self,t):
        #print(Cross(self.tangent(t), self.normal(t)))
        return Cross(self.tangent(t), self.normal(t))
    
    def curvatureArbitrarySpeed(self, t):
        return Norm(self.deriv2(t))
    
    def torsionArbitrarySpeed(self, t):
        numer = Dot(Cross(self.deriv1(t), self.deriv2(t)), self.deriv3(t))
        k = self.curvature(t)
        if k!= 0:
            denom = - k*k
            return numer/denom
        else:
            return 0
    
    def arcLengthArbitrarySpeed(self, t):
        return t - self.t0
    
    #Unit speed
    def tangentUnitSpeed(self, t):
        v = self.deriv1(t)
        if Norm(v) != 0:
            return (ScalMult(1.0/Norm(v), v))
        else:
            return ScalMult(0,v)
        
    def normalUnitSpeed(self, t):
        return Cross(self.binormal(t), self.tangent(t))
    
    def binormalUnitSpeed(self, t):
        v = Cross(self.deriv1(t), self.deriv2(t))
        if Norm(v) != 0:
            return (ScalMult(1.0/Norm(v), v))
        else:
            return ScalMult(0,v)
        
    def curvatureUnitSpeed(self, t):
        v = self.deriv1(t)
        nv = Norm(v)
        numer = Norm(Cross(v, self.deriv2(t)))
        if nv != 0:
            denom = nv*nv*nv
           # print("Yea")
            #print(numer/denom)
            
            return numer/denom
        else:
            return 0.0
    
    def torsionUnitSpeed(self, t):
        v = Cross(self.deriv1(t), self.deriv2(t))
        nv = Norm(v)
        numer = Dot(v, self.deriv3(t))
        if nv != 0:
            denom = nv*nv
            return numer/denom
        else:
            return 0.0
    
    def arcLengthUnitSpeed(self, s):
        length = 0.0
        vlast = self.value(self.t0)
        for i in range(self.arcResolution):
            t = self.t0 + (self.t1 - self.t0)*(i+1) / self.arcResolution
            v = self.value(t)
            length = length + Distance(v, vlast)
            vlast = v
        return length

    def orientedNormal(self, t):
        # For 2D Curves
        t = self.tangent(t)
        return (-t[1], t[0], 0)
    def binormal2d(self, t):
        return (0.0, 0.0, 1.0)
    def torsion2d(self, t):
        return 0.0
    def oCurvatureUnitSpeed(self, t):
        d1 = self.deriv1(t)
        d2 = self.deriv2(t)
        return d1[0]*d2[1] - d1[1]*d2[0]
    def oCurvatureArbitrarySpeed(self, t):
        n = Norm(self.deriv1(t))
        if n!= 0:
            return self.oCurvatureUnitSpeed(t) / (n*n*n)
        else:
            return 0
