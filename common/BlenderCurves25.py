from math import sqrt, cos, sin, pi, radians, degrees
from Vector import *
import Curve
import bpy, mathutils,bmesh


def CurveToEdges(curve, vizparms=None, me=None): #...
    if (vizparms!=None):
        steps = curve.steps
        scale = vizparms.scale
    else:
        steps = 1000
        scale = 1.0

    newmesh = 0
    t0 = curve.t0
    t1 = curve.t1

    oldmats = None

    if (me == None):
        me = bpy.data.meshes.new()
        newmesh = 1
    else:
        if me.materials:
            oldmats = me.materials

    verts = []
    edges = []
    for i in range(steps):#calculate draw position
        #if curve.cyclic:
        #    t = t0 + i * (t1 - t0) / float(steps)
        #else:
        #    t = t0 + i * (t1 - t0) / float(steps - 1)
        verts.append(ScalMult(scale,curve.value(i)))

    for i in range(steps-1):
        edges.append([i, i+1])
    if curve.cyclic:
        edges.append([steps-1, 0])

    me.from_pydata(verts, edges, [])
    if oldmats:
        me.materials = oldmats
    return me

def CurveToTube(curve, name="MyCurve", vizparms=None, me=None, col=None):#converting a curve to a tube
    #print(name)
    new = False
    if (vizparms!=None):
        rad = vizparms.radius
        res = vizparms.radRes
        scale = vizparms.scale
    else:
        steps = 1000
        rad = 0.05
        res = 100
        scale = 1.0
    steps=curve.steps
    rad = 0.02
    res = 6
    t0 = curve.t0
    t1 = curve.t1
    scale=1.0
    oldmats = None


    newme = bpy.data.meshes.new(name+"Mesh")

    if (me):
        for mat in me.materials:
            newme.materials.append(mat)

    verts = []
    faces = []
    uvs = []
    vcol=[]
    #print(res)
    for i in range(steps):
#        if curve.cyclic:
#            t = t0 + i * (t1 - t0) / float(steps)
#        else:
#            t = t0 + i * (t1 - t0) / float(steps - 1)

        v = ScalMult(scale, curve.value(i))
        if Norm(curve.normal(i)) != 0:
            n = ScalMult(1/Norm(curve.normal(i)),curve.normal(i))
        else:
            n = ScalMult(0,curve.normal(i))
        if Norm(curve.binormal(i)) != 0:
            b = ScalMult(1/Norm(curve.binormal(i)),curve.binormal(i))
        else:
            b = ScalMult(0,curve.binormal(i))
        for j in range(res):
            a = 2*pi*j/float(res)
            c = ScalMult(rad * cos(a), n)
            s = ScalMult(rad * sin(a), b)
            offset = Add(c,s)
            verts.append(Add(v, offset))

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

            ve1 = res * i1 + j1
            uv1 = [uu1,vv1]
            ve2 = res * i1 + j2
            uv2 = [uu1,vv2]
            ve3 = res * i2 + j2
            uv3 = [uu2,vv2]
            ve4 = res * i2 + j1
            uv4 = [uu2,vv1]
            faces.append([ve1,ve2,ve3,ve4])
            uvs.append([uv1,uv2,uv3,uv4])
            if col:
                col1 = curve.col(i1)
                col2 = curve.col(i2)
                col3 = curve.col(i2)
                col4 = curve.col(i1)
                vcol.append([col1,col2,col3,col4])
    newme.from_pydata(verts, [], faces)

    bm=bmesh.new()
    bm.from_mesh(newme)
    uv_layer = bm.loops.layers.uv.verify()
    col = col or "colour"
    co_layer = bm.loops.layers.color.new(col)
    for i, f in enumerate(bm.faces):
        this_uv = uvs[i]
        for j, loop in enumerate(f.loops):
            uv_dat = loop[uv_layer].uv
            uv_dat[:] = this_uv[j]

            alpha = 1.0
            new_col = vcol[i][j] + [alpha]
            loop[co_layer] = new_col

    bm.to_mesh(newme)
    bm.free()
    #me.faceUV = True
    #for i, f in enumerate(me.faces):
    #    f.smooth = 1
    #    this_uv = uvs[i]
    #    for j, uv in enumerate(f.uv):
    #        uv[:] = this_uv[j]
    if not col:
        newme.materials.append(bpy.data.materials['Default'])
        mat=bpy.data.materials['Default']
    else:
        # not editing the default colour; this way we know when the colour is weird.
        temp = bpy.data.materials.get(col)
        if not temp:
            mat=bpy.data.materials.new(col)
        else:
            mat = temp
        newme.materials.append(mat)

        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        if nodes.get('Attribute'):
            node_col=nodes.get('Attribute')
        else:
            node_col=nodes.new(type="ShaderNodeAttribute")
        node_col.attribute_name = col
        node_col.location=-200,250

        node_BSDF=nodes.get('Principled BSDF')
        links = mat.node_tree.links
        links.new(node_col.outputs[0], node_BSDF.inputs[0])

    return newme

def CurveToFrenetAction(curve, vizparms=None, action=None, offset=0, toffset=0,
                        Loc=True, Rot=True, preserveDomain=False):
    if (vizparms!=None):
        steps = curve.steps
        scale = vizparms.scale
    else:
        steps = 100
        scale = 1.0
    
    t0 = curve.t0 + toffset
    t1 = curve.t1 + toffset

    start = bpy.context.scene.frame_start
    if curve.cyclic:
        end = bpy.context.scene.frame_end + 1
    else:
        end = bpy.context.scene.frame_end
        
    if not action:
        action = bpy.data.actions.new(name="Frenet")

    if Loc:
        locx = action.fcurves.new(data_path="location", index=0)
        locy = action.fcurves.new(data_path="location", index=1)
        locz = action.fcurves.new(data_path="location", index=2)
        locx.keyframe_points.add(steps)
        locy.keyframe_points.add(steps)
        locz.keyframe_points.add(steps)

    if Rot:
        rotx = action.fcurves.new(data_path="rotation_euler", index=0)
        roty = action.fcurves.new(data_path="rotation_euler", index=1)
        rotz = action.fcurves.new(data_path="rotation_euler", index=2)
        #rotx.keyframe_points.add(steps)
        #roty.keyframe_points.add(steps)
        #rotz.keyframe_points.add(steps)

    for i in range(steps):
        t = i + offset
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

        m = mathutils.Matrix([x,y,z])
        #m[0][0:3] = x
        #m[1][0:3] = y
        #m[2][0:3] = z
        #m[0:3][0] = x
        #m[0:3][1] = y
        #m[0:3][2] = z

        if i > 0:
            e = m.to_euler('ZYX', last_e)
        else:
            e = m.to_euler('ZYX')
        last_e = e
        #ob.setMatrix(m)
        #e = ob.getEuler()
        #ob.setLocation(p)

        if Loc:
            #locx.keyframe_points[i].co = f, p[0]
            #locy.keyframe_points[i].co = f, p[1]
            #locz.keyframe_points[i].co = f, p[2]
            locx.keyframe_points.insert(f, p[0])
            locy.keyframe_points.insert(f, p[1])
            locz.keyframe_points.insert(f, p[2])

        if Rot:
            #rotx.keyframe_points[i].co = f, e.x/10
            #roty.keyframe_points[i].co = f, e.y/10
            #rotz.keyframe_points[i].co = f, e.z/10
            #rotx.keyframe_points.insert(f, e.x/10)
            #roty.keyframe_points.insert(f, e.y/10)
            #rotz.keyframe_points.insert(f, e.z/10)
            rotx.keyframe_points.insert(f, -e.x)
            roty.keyframe_points.insert(f, -e.y)
            rotz.keyframe_points.insert(f, -e.z)

    return action

