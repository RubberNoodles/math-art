import os,bpy

dir = os.path.dirname(bpy.context.blend_data.filepath)+'/..'
bpy.context.scene.render.filepath = f"{dir}/img"

bpy.ops.wm.save_as_mainfile()
