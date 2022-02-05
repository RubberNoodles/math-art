import bpy, mathutils, importlib, os, sys
from math import floor, ceil, pi
from VizParm import VizParms
import MyCurve
importlib.reload(MyCurve)
import BlenderCurves25
importlib.reload(BlenderCurves25)
#Instead of importing all the code, I'm going to move some useful portions, and then copy pasta those cool features afterwards.

def run(curve = None, vizparms = None):
    file=os.path.dirname(bpy.context.blend_data.filepath) + '/curve_data/curve0.txt'
    if not curve:
        curve = MyCurve.MyCurve(file)
    vizparms = vizparms
    name = curve.r_name()

    MakeCurve(curve, vizparms, name)

def MakeCurve(curve, vizparms, name = "MyCurve"):

    try:#Already exist
        ob = bpy.data.objects[name]
        me = ob.data

        if me != None:
            newme = BlenderCurves25.CurveToTube(curve, name, vizparms=vizparms, me=me, col=curve.col_name)
        else:
            newme = BlenderCurves25.CurveToTube(curve, name, vizparms=vizparms, col=curve.col_name)


        newme.validate()
        newme.update()
        ob.data = newme
        bpy.data.meshes.remove(me)

    except Exception as e:#Create new
           me = BlenderCurves25.CurveToTube(curve, vizparms=vizparms, col=curve.col_name)
           ob = bpy.data.objects.new(name,me)
           scn = bpy.context.collection
           scn.objects.link(ob)




