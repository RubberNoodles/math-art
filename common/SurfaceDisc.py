from math import *
from Vector import *
from Surface import *
from Region import *
from CircleRegion import *
from SurfaceRegion import *

class SurfaceDisc(SurfaceRegion):
    def __init__(self, surface, center, radius, phase=0):
        disc = CircleRegion(center, radius, phase)
        SurfaceRegion.__init__(self, surface, disc)
