from math import sqrt, cos, sin, pi

TINY = 0.000000001

def Dot(u, v):
    return (u[0]*v[0] + u[1]*v[1] + u[2]*v[2])

def Norm(v):
    return sqrt(Dot(v, v))

def Add(u, v):
    return (u[0]+v[0], u[1]+v[1], u[2]+v[2])

def Sub(u, v):
    return (u[0]-v[0], u[1]-v[1], u[2]-v[2])

def Distance(u, v):
    return Norm(Sub(u, v))

def ScalMult(a, v):
    return (a*v[0], a*v[1], a*v[2])

def Normalize(v):
    n = Norm(v)
    if (n > TINY):
        return ScalMult(1.0 / n, v)
    return (0.0, 0.0, 0.0)

def Cross(u, v):
    w0 = u[1]*v[2] - u[2]*v[1]
    w1 = u[2]*v[0] - u[0]*v[2]
    w2 = u[0]*v[1] - u[1]*v[0]
    return (w0, w1, w2)
