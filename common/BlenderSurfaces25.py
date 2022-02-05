from math import *
from Vector import *
from Surface import *

#import Blender
#from Blender import Mesh, Object, Material, Mathutils, Ipo, IpoCurve

import bpy, mathutils
import bmesh



def SurfaceToMesh(surface, uSteps, vSteps, me=None, col=None, mat="Default"):
    newmesh = 0

    oldmats = None

    if (me == None):
        me = bpy.data.meshes.new(surface.name+"mesh")
        newmesh = 1
        #oldmats = bpy.data.materials['UV']
    else:
        if me.materials != None:
            oldmats = me.materials
    newme = bpy.data.meshes.new(surface.name+"mesh")
    #me.verts = None # this kills the faces/edges too
    verts = []
    faces = []
    uvs = []
    vcols = []

    for j in range(vSteps):
        for i in range(uSteps):
            (i,j) = (int(i),int(j))
            (x, y, z) = surface.value(i,j)
            verts.append([x,y,z])

    #me.verts.extend(verts)
    #verts = []

    for j in range(vSteps):
        if j == (vSteps-1):
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
            if i == (uSteps-1):
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
                
                #col1 = [surface.red(i,j),surface.green(i,j),surface.blue(i,j)]#getColor(i1, uSteps, j1, vSteps, surface)
                #col2 = [surface.red(i,j),surface.green(i,j),surface.blue(i,j)]#getColor(i2, uSteps, j1, vSteps, surface)
                #col3 = [surface.red(i,j),surface.green(i,j),surface.blue(i,j)]#getColor(i2, uSteps, j2, vSteps, surface)
                #col4 = [surface.red(i,j),surface.green(i,j),surface.blue(i,j)]#getColor(i1, uSteps, j2, vSteps, surface)
                col1 = getColor(i1, uSteps, j1, vSteps, surface)
                col2 = getColor(i2, uSteps, j1, vSteps, surface)
                col3 = getColor(i2, uSteps, j2, vSteps, surface)
                col4 = getColor(i1, uSteps, j2, vSteps, surface)
                #if(i,j) == (100,100):
                    #print(i,j)
                    #print([col1, col2, col3, col4])
               # print([col1, col2, col3, col4])

                vcols.append([col1, col2, col3, col4])

    newme.from_pydata(verts, [], faces)
    bm = bmesh.new()
    bm.from_mesh(newme)
    




    #me.faces.extend(faces)
   # me.calcNormals()
    #vcolors = me.tessface_vertex_colors
    #print('yea')
    #for color in vcolors:
        #print(color)
    #me.faceUV = True
    #if (len(vcols) > 0):
        #me.vertexColors = 1
        
    #for face in bm.faces:
        #for loop in face.loops:
            #uv = loop[uv_lay].uv
            #print("Loop UV: %f, %f" % uv[:])
           # vert = loop.vert
            #print("Loop Vert: (%f,%f,%f)" % vert.co[:])
    uv_layer = bm.loops.layers.uv.verify()
    col = col or "colour"
    co_layer = bm.loops.layers.color.new(col)
    for i, f in enumerate(bm.faces):
        f.smooth = True
        this_uv = uvs[i]
        for j,loop in enumerate(f.loops):
            uv_dat = loop[uv_layer].uv
            uv_dat[:] = this_uv[j]
            #print("yea")
            #print(uv_dat)
            #print(this_uv)
            #print("yea2")

                #uv[:] = this_uv[j]
            
            alpha=1.0
            new_col = vcols[i][j] + [alpha]
            loop[co_layer]=new_col
            #print(j)
            if (len(vcols) > 0):
                #print(i,j)
                #print(vcols[i][j])
                #c.r = vcols[i][j][0]
                #c.g = vcols[i][j][1]
                #c.b = vcols[i][j][2]

                #print(c)
                #f.col[j].a = vcols[i][j][3]
                pass

    bm.to_mesh(newme)
    bm.free()
    #Add the material

    if oldmats:
        #newme.materials=oldmats
        for stuff in oldmats:
            newme.materials.append(stuff)

    if not col:
        newme.materials.append(bpy.data.materials['Default'])
        mat=bpy.data.materials['Default']
    else:
        #Don't edit default colour
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
        node_col.attribute_name = col # Having the same name as the vertex
        # color attribute means that it will inherit the vertex color colors
        # All that remains is to ensure that this material is assigned
        # as the main material. Or give the user the option to choose.
        node_col.location=-200,250

        node_BSDF=nodes.get('Principled BSDF')
        links = mat.node_tree.links
        links.new(node_col.outputs[0], node_BSDF.inputs[0])

    newme.update()
    me.update()
    #newme.vertex_colors.new()

    #color_layer = newme.vertex_colors["Col"]

# or you could avoid using the color_layer name
# color_layer = mesh.vertex_colors.active  

    #i = 0
    #for poly in newme.polygons:
        #for idx in poly.loop_indices:
            #rgb = vcols[0][0]
        #print(rgb)
        #    color_layer.data[i].color = rgb
        #    i += 1
    return newme


#I want to create a function that CHANGES the mesh.

def MeshAnimation(context, verts, uSteps, vSteps):
    ob=context.object.data
    bm=bmesh.new()
    # I need to do a check to make sure the verts array size is the same as the context
    bm.from_mesh(ob)
    i,j=-1,0
    for v in bm.verts:
        i+=1
        if i==uSteps:
            j+=1
            i=0
        if j==vSteps:
            print(v.co)
            break
        v.co.x, v.co.y, v.co.z = verts[i][j]
    bm.to_mesh(ob)
    bm.free()
    return None


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
    try:
        x = float(c) #float(c - c0) / float(c1 - c0)
    except:
        x = 0.0
    if (x > 1.0):
        x = 1.0
    if (x < 0.0):
        x = 0.0
    #print(name)
    #print(x)

    return x

def getColor(i, uSteps, j, vSteps, surface):
    #u = getU(i, uSteps, surface) #recall getU was used in SurfaceToMesh prior to ListData
    #v = getV(j, vSteps, surface)
    u=i
    v=j
    #print(u,v)
    #print(surface.red(u,v))
    r = scaleColor(surface.red(u,v), surface.red0, surface.red1) #Note red0 & red1 is dead code
    g = scaleColor(surface.green(u,v), surface.green0, surface.green1)
    b = scaleColor(surface.blue(u,v), surface.blue0, surface.blue1)

    #return [r, g, b, 255]
    #print([r,g,b])
    #return [r,g,b]
    return [r,g,b]
