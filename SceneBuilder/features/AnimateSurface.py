import bpy, sys, importlib
sys.path.append("")

try:
    import os
    sys.path.append(os.path.dirname(bpy.context.blend_data.filepath))
    sys.path.append(os.path.dirname("/../../common"))
    sys.path.append(os.path.dirname(bpy.context.blend_data.filepath)+"/../../common")
    sys.path.append("C:\Python33\Lib\site-packages")
except:
    pass

import MySurfaceColor
importlib.reload(MySurfaceColor)

import BlenderSurfaces25
importlib.reload(BlenderSurfaces25)


bpy.data.window_managers["WinMan"].animall_properties.key_points = True
bpy.data.window_managers["WinMan"].animall_properties.key_selected = False
# Set up AnimAll Add-on parameters

dir = os.path.dirname(bpy.context.blend_data.filepath)+ '/surf_data'

surface = MySurfaceColor.MySurface(dir+'/surf0.txt')
col=surface.col_name
# Create surface
try:
    ob = bpy.data.objects[surface.return_name()]
    me = ob.data
    if me:
        me = BlenderSurfaces25.SurfaceToMesh(surface, surface.resu, surface.resv, me=me,col=col)
    else:
        me = BlenderSurfaces25.SurfaceToMesh(surface, surface.resu, surface.resv,col=col)
        ob.link(me)
    ob.data=me
except Exception as e:
    me = BlenderSurfaces25.SurfaceToMesh(surface, surface.resu, surface.resv,col=col)
    ob = bpy.data.objects.new(surface.return_name(),me)
    scn = bpy.context.collection
    scn.objects.link(ob)

bpy.context.view_layer.objects.active = ob
ob.select_set(True)

#Start Animating
files = [name for name in os.listdir(dir) if 
    os.path.isfile(os.path.join(dir, name))]
bpy.context.scene.frame_set(0)
frame = 0
bpy.ops.anim.insert_keyframe_animall()
for i in range(1,len(files)):
    data = MySurfaceColor.reshape(dir + '/surf'+str(i)+'.txt')
    verts = data['valueList']
    frame +=20
    
    bpy.context.scene.frame_set(frame)
    BlenderSurfaces25.MeshAnimation(bpy.context, verts, len(verts),len(verts[0]))
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    bpy.ops.anim.insert_keyframe_animall()

bpy.context.scene.frame_end=frame + 20   

bpy.ops.wm.save_as_mainfile()