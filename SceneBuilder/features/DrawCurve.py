# Make sure local modules can be found
import bpy, sys, importlib
try:
    import os
    sys.path.append(os.path.dirname(bpy.context.blend_data.filepath))
    sys.path.append(os.path.dirname("/../../common"))
    sys.path.append(os.path.dirname(bpy.context.blend_data.filepath)+"/../../common")
except:
    pass

# I might be able to reduce this hmmm

import MyCurveRun25
importlib.reload(MyCurveRun25)

from VizParm import VizParms


visparm = VizParms()
MyCurveRun25.run(vizparms = visparm) #Running main program
        

bpy.ops.wm.save_as_mainfile()
#MyCurveRun25.run(visparm)
