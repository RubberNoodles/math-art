from math import sqrt, cos, sin, pi
from Vector import *
import Curve
import Blender
from Blender import Mesh, Object, Material, Mathutils, Ipo, IpoCurve

def CurveToEdges(curve, vizparms=None, me=None):
    if (vizparms!=None):
        steps = vizparms.curveRes
        scale = vizparms.scale
    else:
        steps = 1000
        scale = 1.0

    newmesh = 0
    t0 = curve.t0
    t1 = curve.t1

    oldmats = None
    
    if (me == None):
        me = Mesh.New()
        newmesh = 1
    else:
        if me.materials:
            oldmats = me.materials

    me.verts = None # this kills the faces/edges tooo
    verts = []
    edges = []
    for i in range(steps):
        if curve.cyclic:
            t = t0 + i * (t1 - t0) / float(steps)
        else:
            t = t0 + i * (t1 - t0) / float(steps - 1)
        verts.append(ScalMult(scale,curve.value(t)))
    me.verts.extend(verts)
    verts = []
    for i in range(steps-1):
        edges.append([me.verts[i], me.verts[i+1]])
    if curve.cyclic:
        edges.append([me.verts[steps-1], me.verts[0]])
    me.edges.extend(edges)

    if oldmats:
        me.materials = oldmats
        
    return me

def CurveToTube(curve, vizparms=None, me=None):
    if (vizparms!=None):
        steps = vizparms.curveRes
        rad = vizparms.radius
        res = vizparms.radRes
        scale = vizparms.scale
    else:
        steps = 1000
        rad = 0.05
        res = 4
        scale = 1.0

    newmesh = 0
    t0 = curve.t0
    t1 = curve.t1
        
    oldmats = None
    
    if (me == None):
        me = Mesh.New()
        newmesh = 1
    else:
        if me.materials:
            oldmats = me.materials

    me.verts = None # this kills the faces/edges too
    verts = []
    faces = []
    uvs = []
    
    for i in range(steps):
        if curve.cyclic:
            t = t0 + i * (t1 - t0) / float(steps)
        else:
            t = t0 + i * (t1 - t0) / float(steps - 1)
        v = ScalMult(scale, curve.value(t))
        n = curve.normal(t)
        b = curve.binormal(t)
        for j in range(res):
            a = 2*pi*j/float(res)
            c = ScalMult(rad * cos(a), n)
            s = ScalMult(rad * sin(a), b)
            offset = Add(c,s)
            verts.append(Add(v, offset))
    me.verts.extend(verts)
    verts = []

    for i in range(steps):
        if i == (steps-1):
            if not curve.cyclic:
                continue
            i1 = i
            i2 = 0
        else:
            i1 = i
            i2 = i+1
        if (curve.cyclic):
            uu1 = float(i) / (steps) 
            uu2 = float(i+1) / (steps)
        else:
            uu1 = float(i) / (steps - 1) 
            uu2 = float(i+1) / (steps - 1)

        for j in range(res):
            j1 = j
            j2 = j+1
            if (j2 >= res):
                j2 = 0
            vv1 = float(j) / (res) 
            vv2 = float(j+1) / (res)

            ve1 = me.verts[res * i1 + j1]
            uv1 = [uu1,vv1]
            ve2 = me.verts[res * i1 + j2]
            uv2 = [uu1,vv2]
            ve3 = me.verts[res * i2 + j2]
            uv3 = [uu2,vv2]
            ve4 = me.verts[res * i2 + j1]
            uv4 = [uu2,vv1]
            faces.append([ve1,ve2,ve3,ve4])
            uvs.append([uv1,uv2,uv3,uv4])
        
    me.faces.extend(faces)
    me.calcNormals()

    me.faceUV = True
    for i, f in enumerate(me.faces):
        f.smooth = 1
        this_uv = uvs[i]
        for j, uv in enumerate(f.uv):
            uv[:] = this_uv[j]

    if oldmats:
        me.materials = oldmats
    me.update()

    return me

def CurveToFrenetIpo(curve, vizparms=None, ipo=None, offset=0, toffset=0,
                     Loc=True, Rot=True, preserveDomain=False):
    if (vizparms!=None):
        steps = vizparms.timeRes
        scale = vizparms.scale
    else:
        steps = 100
        scale = 1.0

    t0 = curve.t0 + toffset
    t1 = curve.t1 + toffset

    start = Blender.Get('staframe')
    if curve.cyclic:
        end = Blender.Get('endframe')+1
    else:
        end = Blender.Get('endframe')
        
    if not ipo:
        ipo = Ipo.New("Object", "Frenet")

    if Loc:
        if ipo[Ipo.OB_LOCX]:
            ipo[Ipo.OB_LOCX] = None
        if ipo[Ipo.OB_LOCY]:
            ipo[Ipo.OB_LOCY] = None
        if ipo[Ipo.OB_LOCZ]:
            ipo[Ipo.OB_LOCZ] = None
        locx = ipo.addCurve('LocX') 
        locy = ipo.addCurve('LocY') 
        locz = ipo.addCurve('LocZ')

    if Rot:
        if ipo[Ipo.OB_ROTX]:
            ipo[Ipo.OB_ROTX] = None
        if ipo[Ipo.OB_ROTY]:
            ipo[Ipo.OB_ROTY] = None
        if ipo[Ipo.OB_ROTZ]:
            ipo[Ipo.OB_ROTZ] = None
        rotx = ipo.addCurve('RotX')
        roty = ipo.addCurve('RotY')
        rotz = ipo.addCurve('RotZ')

    for i in range(steps):
        j = i + offset
        t = t0 + j * (t1 - t0) / float(steps - 1)
        if preserveDomain:
            if (t < curve.t0):
                t = curve.t0
            elif (t > curve.t1):
                t = curve.t1
        f = start+ i * (end - start) / float(steps - 1)
        
        p = ScalMult(scale, curve.value(t))
        x = curve.tangent(t)
        y = curve.normal(t)
        z = curve.binormal(t)

        m = Mathutils.Matrix(x,y,z)
        if i > 0:
            e = m.toEuler(last_e)
        else:
            e = m.toEuler()
        last_e = e
        #ob.setMatrix(m)
        #e = ob.getEuler()
        #ob.setLocation(p)

        if Loc:
            locx.append((f,p[0]))
            locy.append((f,p[1]))
            locz.append((f,p[2]))
        if Rot:
            rotx.append((f,e.x/10))
            roty.append((f,e.y/10))
            rotz.append((f,e.z/10))

    if Loc:
        locx.recalc()
        locy.recalc()
        locz.recalc()
    if Rot:
        rotx.recalc()
        roty.recalc()
        rotz.recalc()

    return ipo
