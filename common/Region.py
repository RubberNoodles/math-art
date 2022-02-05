class Region:
    def __init__(self, value, du, dv, u0, u1, v0, v1,
                 uCyclic=False, vCyclic=False):
        self.value = value
        self.du = du
        self.dv = dv
        self.u0 = u0
        self.u1 = u1
        self.v0 = v0
        self.v1 = v1
        self.uCyclic = uCyclic
        self.vCyclic = vCyclic
