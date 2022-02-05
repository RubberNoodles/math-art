from math import *
from Vector import *
from Surface import *

#import Blender
#from Blender import Mesh, Object, Material, Mathutils, Ipo, IpoCurve

import bpy, mathutils, imp

def SurfaceToMesh(surface, uSteps, vSteps, me=None):
    newmesh = 0

    oldmats = None

    if (me == None):
        me = bpy.data.meshes.new("Surface")
        newmesh = 1
    else:
        if me.materials:
            oldmats = me.materials

    #me.verts = None # this kills the faces/edges too
    verts = []
    faces = []
    uvs = []
    vcols = []

    for j in range(vSteps):
        v = getV(j, vSteps, surface)
        for i in range(uSteps):
            u = getU(i, uSteps, surface)
            (x, y, z) = surface.value(u,v)
            verts.append([x,y,z])

    #me.verts.extend(verts)
    verts = []

    for j in range(vSteps):
        if j == (vSteps -1):
            if not surface.vCyclic:
                continue
            j1 = j
            j2 = 0
            vv1 = float(j - 1) / (vSteps - 1)
            vv2 = 1.0
        else:
            j1 = j
            j2 = j+1

        if (surface.vCyclic):
            vv1 = float(j) / (vSteps)
            vv2 = float(j+1) / (vSteps)
        else:
            vv1 = float(j) / (vSteps - 1)
            vv2 = float(j+1) / (vSteps - 1)

        for i in range(uSteps):
            if i == (uSteps -1):
                if not surface.uCyclic:
                    continue
                i1 = i
                i2 = 0
            else:
                i1 = i
                i2 = i+1

            if (surface.uCyclic):
                uu1 = float(i) / (uSteps)
                uu2 = float(i+1) / (uSteps)
            else:
                uu1 = float(i) / (uSteps - 1)
                uu2 = float(i+1) / (uSteps - 1)

            ve1 = j1 * uSteps + i1
            uv1 = [uu1,vv1]
            ve2 = j1 * uSteps + i2
            uv2 = [uu2,vv1]
            ve3 = j2 * uSteps + i2
            uv3 = [uu2,vv2]
            ve4 = j2 * uSteps + i1
            uv4 = [uu1,vv2]

            faces.append([ve1,ve2,ve3,ve4])
            uvs.append([uv1,uv2,uv3,uv4])
            if (surface.red):
                col1 = getColor(i1, uSteps, j1, vSteps, surface)
                col2 = getColor(i2, uSteps, j1, vSteps, surface)
                col3 = getColor(i2, uSteps, j2, vSteps, surface)
                col4 = getColor(i1, uSteps, j2, vSteps, surface)
                vcols.append([col1, col2, col3, col4])

    #me.faces.extend(faces)
   # me.calcNormals()

    me.faceUV = True
    if (len(vcols) > 0):
        me.vertexColors = 1
    for i, f in enumerate(me.faces):
        f.smooth = 1
        this_uv = uvs[i]
        for j, uv in enumerate(f.uv):
            uv[:] = this_uv[j]
            if (len(vcols) > 0):
                f.col[j].r = vcols[i][j][0]
                f.col[j].g = vcols[i][j][1]
                f.col[j].b = vcols[i][j][2]
                f.col[j].a = vcols[i][j][3]

    me.from_pydata(verts, [], faces)

    if oldmats:
        me.materials = oldmats

    me.update()

    return me

def SurfaceToTransformation(surface, u, v, ob, Loc=True, Rot=True,
                            last_e = None):
    if (Rot):
        x = Normalize(surface.du(u,v))
        y = surface.normal(u,v)
        z = Cross(x, y)
        m = Mathutils.Matrix(x,y,z)

        if (last_e):
            e = m.toEuler(last_e)
        else:
            e = m.toEuler()
        last_e = e

        ob.setEuler([x * (pi/180) for x in e])

    if (Loc):
        ob.setLocation(surface.value(u,v))

def getV(j, vSteps, surface):
    v0 = surface.v0
    v1 = surface.v1

    if surface.vCyclic:
        return (v0 + j * (v1 - v0) / float(vSteps))
    else:
        return (v0 + j * (v1 - v0) / float(vSteps - 1))

def getU(i, uSteps, surface):
    u0 = surface.u0
    u1 = surface.u1

    if surface.uCyclic:
        return (u0 + i * (u1 - u0) / float(uSteps))
    else:
        return (u0 + i * (u1 - u0) / float(uSteps - 1))

def scaleColor(c, c0, c1):
    x = float(c - c0) / float(c1 - c0)
    if (x > 1.0):
        x = 1.0
    if (x < 0.0):
        x = 0.0
    return int(255*x)

def getColor(i, uSteps, j, vSteps, surface):
    u = getU(i, uSteps, surface)
    v = getV(j, vSteps, surface)
    r = scaleColor(surface.red(u,v), surface.red0, surface.red1)
    g = scaleColor(surface.green(u,v), surface.green0, surface.green1)
    b = scaleColor(surface.blue(u,v), surface.blue0, surface.blue1)

    return [r, g, b, 255]

