from math import sqrt, cos, sin, pi, radians, degrees
from Vector import *
import ODE
import bpy, mathutils

def PointsToAction(Para = ODE,x=0,y = 0, z = 0, action=None, res = 1000):
    if not action:
        action = bpy.data.actions.new(name="VField")
    #print(ListOfData)

    locx = action.fcurves.new(data_path="location", index=0)
    locy = action.fcurves.new(data_path="location", index=1)
    locz = action.fcurves.new(data_path="location", index=2)
    locx.keyframe_points.add(res)
    locy.keyframe_points.add(res)
    locz.keyframe_points.add(res)
    u = x
    v = y
    w = z

    Data = ODE.Data(u,v,w)
    for i in range(res):
        locx.keyframe_points.insert(i, u)
        locy.keyframe_points.insert(i, v)
        locz.keyframe_points.insert(i, w)
        u = u+ 1/60*Data.locx
        v = v+ 1/60*Data.locy
        w = w+ 1/60*Data.locz
        Data = ODE.Data(u,v,w)
        #print(u,v,w)

    return action
def PointsToField(Para = ODE):
    tail_points = []
    tip_points = []

    #arrow_mesh = bpy.data.meshes["arrow_mesh"]
    scene = bpy.context.scene
    objects = bpy.data.objects

    for i in range(10):
        for j in range(10):
            tail_points.append((2*i,2*j,0))
            tail_points.append((-2*i,-2*j,0))
            tail_points.append((-2*i,2*j,0))
            tail_points.append((2*i,-2*j,0))

    for vector in tail_points:
        result = ODE.Data(vector[0],vector[1],vector[2])
        tip_points.append((vector[0] + 1/60*result.locx,vector[1] + 1/60*result.locy,vector[2] + 1/60*result.locz))

    #print(tail_points,tip_points)
    #scene = bpy.context.scene
    

    arrow_stem_mesh = objects['Arrow_cone.001'].data
    #arrow_cone_mesh = objects['Arrow_cone'].data
    arrow_cone_height = 0.448  # for example..

    #vectors = [
   #[(0,0,1), (0,0,0)],
   #[(0,1,0), (0,0,0)],
  # [(1,0,0), (0,0,0)],
  # [(1,1,1), (0,0,0)],
  # [(2,2,2), (3,3,3)],
 #  [(4,4,2), (2,2,2)],
 #  [(4,4,3), (2,0,0)]
#]
    i = 0
    for i in range(len(tip_points)):
        head = tip_points[i]
        tail = tail_points[i]
        v1, v2 = mathutils.Vector(head), mathutils.Vector(tail)

    # Scale the Stem, and add to scene
        try:
            new = False
            obj = bpy.data.objects["Arrow_duplicate"+str(i)]



        except:
            new = True
            obj = bpy.data.objects.new("Arrow_duplicate"+str(i), arrow_stem_mesh)

        obj.location = v2
            #obj.scale = (1, 1., 1)
        obj.rotation_mode = 'QUATERNION'
        obj.rotation_quaternion = (v1-v2).to_track_quat('Z','Y')
        if(new):
            scene.objects.link(obj)
    
    # orient Cone, and add to scene
        #obj2 = bpy.data.objects.new("Tio_duplicate"+str(i), arrow_cone_mesh)
        #obj2.location = v1   # start at tail and work back
        #obj2.rotation_mode = 'QUATERNION'
        #obj2.rotation_quaternion = (v1-v2).to_track_quat('Z','Y')
        #scene.objects.link(obj2)
       #print(i)
    #i = 0
    #for tail in tail_points:
        #for head in tip_points:
           # v1, v2 = mathutils.Vector(head), mathutils.Vector(tail)

    # duplicate mesh into new object.
        #name = "Arrow_duplicate" + str(i)
        
        #obj = bpy.data.objects.new(name, arrow_mesh) 

        #obj.location = v2
       # obj.scale = (0.15,0.15,-0.5)
        #obj.rotation_mode = 'QUATERNION'
        #obj.rotation_quaternion = (v1-v2).to_track_quat('Z','Y')

        #scene.objects.link(obj)
        #i += 1
def PointsToTrace(Para = ODE, depth = 1, x=0,y=0,z=0, action=None): #para = linearized local solution, depth = how many steps the crumbs go
    if not action:
        action = bpy.data.actions.new(name="VField")
    #print(ListOfData)

    locx = action.fcurves.new(data_path="location", index=0)
    locy = action.fcurves.new(data_path="location", index=1)
    locz = action.fcurves.new(data_path="location", index=2)
    locx.keyframe_points.add(depth)
    locy.keyframe_points.add(depth)
    locz.keyframe_points.add(depth)
    u = x
    v = y
    w = z

    Data = ODE.Data(u,v,w)
    for i in range(depth):
        locx.keyframe_points.insert(1*i, u)
        locy.keyframe_points.insert(1*i, v)
        locz.keyframe_points.insert(1*i, w)
        u = u+ 1/60*Data.locx
        v = v+ 1/60*Data.locy
        w = w+ 1/60*Data.locz
        Data = ODE.Data(u,v,w)
        
    return [action,(u,v,w)]