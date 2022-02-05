import bpy, sys

sys.path.append("")
try:
    import os
    sys.path.append(os.path.dirname(bpy.context.blend_data.filepath))
    sys.path.append(os.path.dirname(bpy.context.blend_data.filepath)+"/../../common")
except:
    pass

import MySurfaceColor
import BlenderSurfaces25
import MyCurveRun25


argv=sys.argv
argv = argv[argv.index('--')+1:]
coordU = int(argv[0])
coordV = int(argv[1])
bpy.context.scene.frame_set(0)

#----
# Constant temporarily; I need to figure out how to make it can read multiple files easily
file_path= os.path.dirname(bpy.context.blend_data.filepath)+ '/surf_data/surf0.txt'
surface = MySurfaceColor.MySurface(file_path)

try:
    ob = bpy.data.objects[surface.return_name()]
    me = ob.data
    if me:
        me = BlenderSurfaces25.SurfaceToMesh(surface, surface.resu, surface.resv, me=me,col=surface.col_name)
    else:
        me = BlenderSurfaces25.SurfaceToMesh(surface, surface.resu, surface.resv,col=surface.col_name)
        ob.link(me)
    ob.data=me
except Exception as e:
    me = BlenderSurfaces25.SurfaceToMesh(surface, surface.resu, surface.resv, col=surface.col_name)
    ob = bpy.data.objects.new(surface.return_name()+"Surface",me)
    scn = bpy.context.collection
    scn.objects.link(ob)

uSteps=surface.resu
vSteps=surface.resv
if coordU:
    for i in range(coordU):
        curveU = MySurfaceColor.SurfaceToCoordinateLine(file_path, uv = 'U', name0=f'{i}', ind = (i)*uSteps//(coordU-1))
        MyCurveRun25.run(curveU)
if coordV:
    for i in range(coordV):
        curveV = MySurfaceColor.SurfaceToCoordinateLine(file_path, uv = 'V', name0=f'{i}', ind = (i+1)*uSteps//(coordV-1))
        MyCurveRun25.run(curveV)

ob.name = surface.return_name()

bpy.ops.wm.save_as_mainfile()





